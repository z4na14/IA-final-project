import numpy as np
import matplotlib.pyplot as plt
import sys
import json
import os
from components.Map import Map
from components.Boundaries import Boundaries
from components.SearchEngine import build_graph, path_finding, compute_path_cost, h1, h2


def plot_radar_locations(boundaries: Boundaries,
                         radar_locations: np.array,
                         title: str = "Radar Locations in the Map") -> None:
    """
    Plots radar locations
    Arguments:
        boundaries: Geographic boundaries object
        radar_locations: Numpy array of (lat, lon) coordinates
        title: Optional plot title
    """
    plt.figure(figsize=(10, 8))
    plt.title(title)

    # Plot map boundaries
    plt.plot([boundaries.min_lon, boundaries.max_lon, boundaries.max_lon, boundaries.min_lon, boundaries.min_lon],
             [boundaries.max_lat, boundaries.max_lat, boundaries.min_lat, boundaries.min_lat, boundaries.max_lat],
             'k--', linewidth=1, label='Area Boundary')

    # Plot radars
    plt.scatter(radar_locations[:, 1], radar_locations[:, 0],
                c='red', marker='X', s=100, label='Radars', zorder=3)

    # Style settings
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.grid(True, alpha=0.3)
    plt.legend(loc='upper right')
    plt.tight_layout()
    plt.show()
    return

def plot_detection_fields(detection_map: np.array,
                          boundaries: Boundaries,
                          title: str = "Radar Detection Fields",
                          bicubic: bool = True) -> None:
    """
    Plots detection fields
    Arguments:
        detection_map: 2D numpy array of detection probabilities
        boundaries: Geographic boundaries object
        title: Optional plot title
        bicubic: Whether to use smooth interpolation
    """
    plt.figure(figsize=(10, 8))
    plt.title(title)

    # Set up geographic extent
    extent = [boundaries.min_lon, boundaries.max_lon,
              boundaries.min_lat, boundaries.max_lat]

    # Plot detection map
    im = plt.imshow(detection_map,
                    extent=extent,
                    origin='lower',
                    cmap='RdYlGn_r',  # Red-Yellow-Green (reversed)
                    vmin=0, vmax=1,
                    alpha=0.8,
                    interpolation='bicubic' if bicubic else None)

    # Add colorbar and labels
    cbar = plt.colorbar(im)
    cbar.set_label('Detection Probability')
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.grid(True, alpha=0.3)

    # Plot boundaries
    plt.plot([boundaries.min_lon, boundaries.max_lon, boundaries.max_lon, boundaries.min_lon, boundaries.min_lon],
             [boundaries.max_lat, boundaries.max_lat, boundaries.min_lat, boundaries.min_lat, boundaries.max_lat],
             'k--', linewidth=1)

    plt.legend(loc='upper right')
    plt.tight_layout()
    plt.show()
    return

def plot_solution(detection_map: np.array,
                  solution_plan: list,
                  boundaries: Boundaries,
                  bicubic: bool = True) -> None:
    """
    Plots the solution plan over the detection map
    Arguments:
        detection_map: 2D numpy array of detection probabilities
        solution_plan: List of path segments (from path_finding)
        boundaries: Boundaries object containing geographic limits
        bicubic: Whether to use bicubic interpolation for smoother visualization
    """
    plt.figure(figsize=(10, 8))
    plt.title("Optimal Path Through Radar Detection Field")

    # Set up geographic extent
    extent = [boundaries.min_lon, boundaries.max_lon,
              boundaries.min_lat, boundaries.max_lat]

    # Plot detection map first
    im = plt.imshow(detection_map,
                    extent=extent,
                    origin='lower',
                    cmap='RdYlGn_r',  # Red-Yellow-Green (reversed)
                    vmin=0, vmax=1,
                    alpha=0.7,
                    interpolation='bicubic' if bicubic else None)

    # Plot each path segment
    for segment in solution_plan:
        if not segment:
            continue

        # Extract coordinates
        lons = [point['geo'][1] for point in segment]
        lats = [point['geo'][0] for point in segment]

        # Plot path
        plt.plot(lons, lats, 'b-', linewidth=2, zorder=3)

        # Plot markers
        plt.scatter(lons[0], lats[0], c='green', marker='o', s=100, zorder=4)
        plt.scatter(lons[-1], lats[-1], c='red', marker='X', s=100, zorder=4)

    # Add colorbar and labels
    cbar = plt.colorbar(im)
    cbar.set_label('Detection Probability')
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.grid(True, alpha=0.3)

    # Create custom legend
    legend_elements = [
        plt.Line2D([0], [0], color='blue', lw=2, label='Flight Path'),
        plt.scatter([], [], c='green', marker='o', s=100, label='Path Start'),
        plt.scatter([], [], c='red', marker='X', s=100, label='Path End')
    ]
    plt.legend(handles=legend_elements, loc='upper right')

    plt.tight_layout()
    plt.show()
    return

def parse_args() -> dict:
    """ Parses the main arguments of the program and returns them stored in a dictionary """
    json_path            = f"{os.getcwd()}/src/main/python/components/scenarios.json"
    scenario_json        = sys.argv[1]
    tolerance            = float(sys.argv[2])
    execution_parameters = {}

    # Depending on execution type, path can be different
    try:
        with open(json_path, 'r', encoding='utf-8') as file:
            execution_parameters = retrieve_file_info(execution_parameters, file, scenario_json)

    # Fallback if ran inside the main folder
    except FileNotFoundError:
        alternative_json_path = f"{os.getcwd()}/components/scenarios.json"
        with open(alternative_json_path, 'r', encoding='utf-8') as file:
            execution_parameters = retrieve_file_info(execution_parameters, file, scenario_json)

    execution_parameters["tolerance"] = tolerance
    return execution_parameters

def retrieve_file_info(execution_parameters, file, scenario_json):
    """
    Retrieves information from file, to avoid duplicate code inside the function
    Arguments:
        execution_parameters: Dictionary of execution parameters
        file: File descriptor from context manager
        scenario_json: Path to the scenario json file
    """
    data = json.load(file)
    for entry in data:
        key = list(entry.keys())[0]
        if key == scenario_json:
            execution_parameters = entry[key]
            break
    return execution_parameters


# System's main function
def main() -> None:
    # Parse the input parameters (arguments) of the program (current execution)
    execution_parameters = parse_args()

    # Set the pseudo-random number generator seed (DO NOT MODIFY)
    np.random.seed(42)

    # Set boundaries
    boundaries = Boundaries(max_lat=execution_parameters['max_lat'],
                            min_lat=execution_parameters['min_lat'],
                            max_lon=execution_parameters['max_lon'],
                            min_lon=execution_parameters['min_lon'])
    
    # Define the map with its corresponding boundaries and coordinates
    radar_map = Map(boundaries=boundaries,
            height=execution_parameters['H'],
            width=execution_parameters['W'])
    
    # Generate random radars
    n_radars = execution_parameters['n_radars']
    radar_map.generate_radars(n_radars=n_radars)
    radar_locations = radar_map.get_radars_locations_numpy()

    # Plot the radar locations (latitude increments from bottom to top)
    plot_radar_locations(boundaries=boundaries, radar_locations=radar_locations)

    # Compute the detection map (sets the costs for each cell)
    detection_map = radar_map.compute_detection_map()

    # Plot the detection map (detection fields)
    plot_detection_fields(detection_map=detection_map, boundaries=boundaries)

    # Build the graph from the detection map
    directed_graph = build_graph(detection_map=detection_map, tolerance=execution_parameters['tolerance'])

    # Get the POI's that the plane must visit
    points_of_interest = np.array(execution_parameters['POIs'], dtype=np.float32)

    # Compute the solution
    solution_plan, nodes_expanded = path_finding(graph=directed_graph,
                                                 heuristic_function=h1,
                                                 locations=points_of_interest,
                                                 initial_location_index=0,
                                                 boundaries=boundaries,
                                                 map_width=radar_map.width,
                                                 map_height=radar_map.height)
    
    # Compute the solution cost
    path_cost = compute_path_cost(graph=directed_graph, solution_plan=solution_plan)

    # Some verbose of the total cost and the number of expanded nodes
    print(f"Total path cost: {path_cost}")
    print(f"Number of expanded nodes: {nodes_expanded}")

    # Plot the solution
    plot_solution(detection_map=detection_map, boundaries=boundaries, solution_plan=solution_plan)

if __name__ == '__main__':
    main()
