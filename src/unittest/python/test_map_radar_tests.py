"""Contains the test cases execution of the radar pathfinder"""
import os
import unittest
import json
import sys
from ast import literal_eval
from pathlib import Path
import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../main/python")))
from main import main
from components.Map import Map, Boundaries
from components.SearchEngine import path_finding, build_graph, h1

class TestRadarPathfinder(unittest.TestCase):
    """Class for testing the Radar Pathfinder system"""

    @classmethod
    def setUpClass(cls):
        # Handle working directory setup
        working_directory = Path.cwd().parts
        if working_directory[-1] == "data" or working_directory[-1] == "python":
            os.chdir("../../../")

        # Load all test cases from JSON file
        try:
            test_file = Path("./src/unittest/data/test_cases.json")
            with open(test_file, mode="r", encoding='UTF-8') as file:
                cls.test_data = json.load(file)["test_cases"]
        except FileNotFoundError as exception:
            raise RuntimeError("Test cases file not found") from exception
        except json.JSONDecodeError as exception:
            raise RuntimeError("Invalid test cases JSON format") from exception

        # Change directory to components folder to store and retrieve the cached information from there
        os.chdir("./src/main/python")

    def test_radar_pathfinder_scenarios(self):
        """Run all test cases dynamically from JSON data."""
        for case in self.test_data:
            with self.subTest(case_id=case["test_case_id"]):
                # Prepare system arguments
                sys.argv = ["main.py", case["scenario"], str(case["tolerance"]), "-d"]

                with self.assertRaises(eval(case["expected_error"].split(":")[0])):
                    # Execute main function
                    main()
                    self.assertIn(case["expected_error"], str(context.exception))

    def test_map_components(self):
        """Additional component-level tests"""
        np.random.seed(42)

        # Test Case 6: POI in no-fly zone
        bounds = Boundaries(37.0, 36.0, -115.0, -116.0)
        test_map = Map(bounds, 10, 10)
        test_map.generate_radars(5)
        points_of_interest = np.array([[37.21979775, -115.88858433],
                                       [37.21979775, -115.81969089]],
                                      dtype=np.float32)
        detection_map = test_map.compute_detection_map(use_cache=False)
        directed_graph = build_graph(detection_map=detection_map, tolerance=0.01)

        with self.assertRaises(RuntimeError):
            path_finding(graph=directed_graph,
                         heuristic_function=h1,
                         locations=points_of_interest,
                         initial_location_index=0,
                         boundaries=bounds,
                         map_width=16,
                         map_height=16)
            self.assertIn("Pathfinding aborted due to invalid path segment", str(context.exception))

if __name__ == '__main__':
    unittest.main()