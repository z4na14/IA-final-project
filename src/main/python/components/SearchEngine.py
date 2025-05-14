import numpy as np
import networkx as nx
from .Boundaries import Boundaries
from tqdm import tqdm


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
    """Builds a directed graph from the detection map with proper node validation"""
    if tolerance <= 1e-4:
        raise ValueError("Tolerance must be greater than 1e-4")
    elif tolerance > 1:
        raise ValueError("Tolerance must be between 1e-4 and 1")
    elif tolerance == None:
        raise ValueError("Missing required tolerance argument")
    elif type(tolerance) != np.float32 and type(tolerance) != float:
        raise TypeError("Tolerance must be numeric")


    graph = nx.DiGraph()
    height, width = detection_map.shape

    # First pass: Add all nodes to ensure complete coordinate space
    for y in range(height):
        for x in range(width):
            if detection_map[y, x] <= tolerance:
                graph.add_node((int(y), int(x)))

    # Second pass: Connect valid edges
    for y in range(height):
        for x in range(width):
            current = (y, x)

            # Skip if current node is above tolerance
            if detection_map[y, x] > tolerance:
                continue

            # Check all 4 possible neighbors
            for distance_y, distance_x in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                neighbour_y, neighbour_x = y + distance_y, x + distance_x

                # Validate neighbor coordinates
                if 0 <= neighbour_y < height and 0 <= neighbour_x < width:
                    neighbor = (neighbour_y, neighbour_x)

                    # Only add edge if destination is below tolerance
                    if detection_map[neighbour_y, neighbour_x] <= tolerance:
                        graph.add_edge(current, neighbor, weight=detection_map[neighbour_y, neighbour_x])

    # Verify graph connectivity
    if graph.number_of_nodes() == 0:
        raise ValueError("Empty graph - all nodes exceed tolerance")

    return graph

def discretize_coords(high_level_plan: np.array, boundaries: Boundaries,
                      map_width: np.int32, map_height: np.int32) -> np.array:
    """Converts coordinates with boundary checking"""
    discretized = []
    for lat, lon in high_level_plan:
        # Clamp coordinates to valid range first
        lat = np.clip(lat, boundaries.min_lat, boundaries.max_lat)
        lon = np.clip(lon, boundaries.min_lon, boundaries.max_lon)

        # Then discretize
        norm_lat = (lat - boundaries.min_lat) / (boundaries.max_lat - boundaries.min_lat)
        norm_lon = (lon - boundaries.min_lon) / (boundaries.max_lon - boundaries.min_lon)

        x = int(norm_lon * (map_width - 1))
        y = int(norm_lat * (map_height - 1))

        # Ensure we stay within grid bounds
        x = np.clip(x, 0, map_width - 1)
        y = np.clip(y, 0, map_height - 1)

        discretized.append((y, x))
    return np.array(discretized)

def path_finding(graph: nx.DiGraph,
                 heuristic_function,
                 locations: np.array,
                 initial_location_index: np.int32,
                 boundaries: Boundaries,
                 map_width: np.int32,
                 map_height: np.int32) -> tuple:
    """Robust path finding with coordinate validation and error handling"""
    global NODES_EXPANDED

    try:
        # Discretize coordinates with boundary checking
        discretized_locations = discretize_coords(locations, boundaries, map_width, map_height)
        # Convert to list of tuples with native Python ints
        discretized_locations = [(int(y), int(x)) for y, x in discretized_locations]
    except Exception as error:
        raise ValueError(f"Coordinate discretization failed: {str(error)}")

    if len(discretized_locations) <= 1:
        raise ValueError("At least 2 POIs required for pathfinding")

    solution_plan = []
    total_nodes_expanded = 0
    has_invalid_path = False

    # Visit POIs in sequence
    for i in tqdm(range(initial_location_index, len(discretized_locations) - 1), desc="Finding path between POIs"):
        start = discretized_locations[i]
        end = discretized_locations[i + 1]

        # Validate nodes exist in graph
        if start not in graph:
            print(f"Warning: Target node {start} not in graph (possibly in no-fly zone)")
            has_invalid_path = True
            break
        if end not in graph:
            print(f"Warning: Target node {end} not in graph (possibly in no-fly zone)")
            has_invalid_path = True
            break

        try:
            NODES_EXPANDED = 0  # Reset counter

            # Find path with type-safe coordinates
            path = nx.astar_path(graph,
                                tuple(start),  # Ensure tuple type
                                tuple(end),
                                heuristic=heuristic_function,
                                weight='weight')

            # Convert path to include both coordinate systems
            path_segment = []
            for y, x in path:
                lat = boundaries.min_lat + (y / (map_height - 1)) * (boundaries.max_lat - boundaries.min_lat)
                lon = boundaries.min_lon + (x / (map_width - 1)) * (boundaries.max_lon - boundaries.min_lon)

                path_segment.append({
                    'grid': (int(y), int(x)),  # Ensure native ints
                    'geo': (float(lat), float(lon))
                })

            solution_plan.append(path_segment)
            total_nodes_expanded += NODES_EXPANDED

        except nx.NetworkXNoPath:
            print(f"No valid path from {start} to {end}")
            has_invalid_path = True
            break

        except Exception as error:
            print(f"Pathfinding failed between {start} and {end}: {str(error)}")
            has_invalid_path = True
            break

    if total_nodes_expanded == 0:
        raise RuntimeError("Empty graph - all nodes exceed tolerance")

    if has_invalid_path: raise RuntimeError("Pathfinding aborted due to invalid path segment")

    return solution_plan, total_nodes_expanded

def compute_path_cost(graph: nx.DiGraph, solution_plan: list) -> np.float32:
    """ Computes the total cost of the whole planning solution """
    total_cost = 0.0

    for path_segment in solution_plan:
        for i in range(len(path_segment) - 1):
            start = path_segment[i]['grid']
            end = path_segment[i+1]['grid']
            total_cost += graph[start][end]['weight']

    return total_cost