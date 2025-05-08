import numpy as np
import networkx as nx
from .Boundaries import Boundaries

# Number of nodes expanded in the heuristic search (stored in a global variable to be updated from the heuristic functions)
NODES_EXPANDED = 0

def h1(current_node, objective_node) -> np.float32:
    """ First heuristic to implement - Euclidean distance """
    global NODES_EXPANDED
    h = np.sqrt((current_node[0] - objective_node[0])**2 + (current_node[1] - objective_node[1])**2)
    NODES_EXPANDED += 1
    return h

def h2(current_node, objective_node) -> np.float32:
    """ Second heuristic to implement - Manhattan distance """
    global NODES_EXPANDED
    h = abs(current_node[0] - objective_node[0]) + abs(current_node[1] - objective_node[1])
    NODES_EXPANDED += 1
    return h

def build_graph(detection_map: np.array, tolerance: np.float32) -> nx.DiGraph:
    """ Builds an adjacency graph (not an adjacency matrix) from the detection map """
    directer_graph = nx.DiGraph()
    height, width = detection_map.shape

    for i in range(height):
        for j in range(width):
            # Only add nodes with detection probability <= tolerance
            if detection_map[i, j] <= tolerance:
                # If node was already added by function add_edge, DiGraph implementation won't throw any errors
                directer_graph.add_node((i, j))

                # Check all 4 possible neighbors
                for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    ni, nj = i + di, j + dj
                    if 0 <= ni < height and 0 <= nj < width and detection_map[ni, nj] <= tolerance:
                        # Edge weight is the detection probability of the destination node
                        directer_graph.add_edge((i, j), (ni, nj), weight=detection_map[ni, nj])

    return directer_graph

def discretize_coords(high_level_plan: np.array, boundaries: Boundaries, map_width: np.int32, map_height: np.int32) -> np.array:
    """ Converts coordiantes from (lat, lon) into (x, y) """
    discretized = []

    for lat, lon in high_level_plan:
        # Normalize coordinates to [0, 1] range
        norm_lat = (lat - boundaries.min_lat) / (boundaries.max_lat - boundaries.min_lat)
        norm_lon = (lon - boundaries.min_lon) / (boundaries.max_lon - boundaries.min_lon)

        # Scale to grid dimensions
        x = int(norm_lon * (map_width - 1))
        y = int(norm_lat * (map_height - 1))

        discretized.append((y, x))  # Using (row, col) convention

    return np.array(discretized)

def path_finding(G: nx.DiGraph,
                 heuristic_function,
                 locations: np.array,
                 initial_location_index: np.int32,
                 boundaries: Boundaries,
                 map_width: np.int32,
                 map_height: np.int32) -> tuple:
    """ Implementation of the main searching / path finding algorithm """
    global NODES_EXPANDED

    # Discretize the POIs coordinates
    discretized_locations = discretize_coords(locations, boundaries, map_width, map_height)

    solution_plan = []
    total_nodes_expanded = 0

    # Visit all POIs in order starting from initial_location_index
    current_location = discretized_locations[initial_location_index]

    for i in range(initial_location_index + 1, len(discretized_locations)):
        next_location = discretized_locations[i]

        try:
            # Reset nodes expanded counter
            NODES_EXPANDED = 0

            # Find path using A* with the specified heuristic
            path = nx.astar_path(G, tuple(current_location), tuple(next_location),
                                 heuristic=heuristic_function, weight='weight')

            # Add path to solution plan (converting back to lat/lon)
            path_coords = []
            for y, x in path:
                lat = boundaries.min_lat + (y / (map_height - 1)) * (boundaries.max_lat - boundaries.min_lat)
                lon = boundaries.min_lon + (x / (map_width - 1)) * (boundaries.max_lon - boundaries.min_lon)
                path_coords.append(f"[{lat}, {lon}]")

            solution_plan.append(path_coords)
            total_nodes_expanded += NODES_EXPANDED

            # Move to next location
            current_location = next_location

        except nx.NetworkXNoPath:
            print(f"No path found from {current_location} to {next_location}")
            return None, 0

    return solution_plan, total_nodes_expanded

def compute_path_cost(G: nx.DiGraph, solution_plan: list) -> np.float32:
    """ Computes the total cost of the whole planning solution """
    total_cost = 0.0

    for path in solution_plan:
        for i in range(len(path) - 1):
            # Get edge weight between consecutive nodes
            start = eval(path[i])
            end = eval(path[i+1])
            total_cost += G[start[0], start[1]][end[0], end[1]]['weight']

    return total_cost