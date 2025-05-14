from tqdm import tqdm
import numpy as np
import os
import pickle
import hashlib
from datetime import datetime

from .Location import Location
from .Boundaries import Boundaries
from .Radar import Radar


# Constant that avoids setting cells to have an associated cost of zero
EPSILON = 1e-4

class Map:
    """ Class that models the map for the simulation """
    def __init__(self,
                 boundaries: Boundaries,
                 height:     np.int32,
                 width:      np.int32,
                 radars:     np.array=None):
        self.boundaries = boundaries        # Boundaries of the map
        self.height     = height            # Number of coordinates in the y-axis
        self.width      = width             # Number of coordinates int the x-axis
        self.radars     = radars            # List containing the radars (objects)

        # Setup cache directory
        self.cache_dir = os.path.join(os.path.dirname(__file__), 'map_cache')
        os.makedirs(self.cache_dir, exist_ok=True)

    def generate_radars(self, n_radars: np.int32) -> None:
        """ Generates n-radars randomly and inserts them into the radars list """
        # Select random coordinates inside the boundaries of the map
        lat_range = np.linspace(start=self.boundaries.min_lat,
                                stop=self.boundaries.max_lat, num=self.height)
        lon_range = np.linspace(start=self.boundaries.min_lon,
                                stop=self.boundaries.max_lon, num=self.width)
        rand_lats = np.random.choice(a=lat_range, size=n_radars, replace=False)
        rand_lons = np.random.choice(a=lon_range, size=n_radars, replace=False)
        self.radars = []        # Initialize 'radars' as an empty list

        # Loop for each radar that must be generated
        for i in range(n_radars):
            # Create a new radar
            new_radar = Radar(location=Location(latitude=rand_lats[i], longitude=rand_lons[i]),
                              transmission_power=np.random.uniform(low=1, high=1000000),
                              antenna_gain=np.random.uniform(low=10, high=50),
                              wavelength=np.random.uniform(low=0.001, high=10.0),
                              cross_section=np.random.uniform(low=0.1, high=10.0),
                              minimum_signal=np.random.uniform(low=1e-10, high=1e-15),
                              total_loss=np.random.randint(low=1, high=10),
                              covariance=None)

            # Insert the new radar
            self.radars.append(new_radar)

    def get_radars_locations_numpy(self) -> np.array:
        """ Returns an array with the coordiantes (lat, lon) of each radar registered in the map """
        locations = np.zeros(shape=(len(self.radars), 2), dtype=np.float32)
        for i in range(len(self.radars)):
            locations[i] = self.radars[i].location.to_numpy()
        return locations

    def compute_detection_map(self, use_cache: bool = True) -> np.array:
        """Computes or loads detection map with caching support"""
        # Generate unique cache key based on map parameters
        cache_key = self._generate_cache_key()
        cache_file = os.path.join(self.cache_dir, f"{cache_key}.pkl")

        # Try loading from cache
        if use_cache and os.path.exists(cache_file):
            try:
                with open(cache_file, 'rb') as f:
                    print(f"Loading cached detection map from {cache_file}")
                    return pickle.load(f)
            except Exception as e:
                print(f"Cache load failed: {e}. Recomputing...")

        # Compute fresh if no cache exists or loading failed
        print("Computing new detection map...")
        detection_map = self._compute_fresh_detection_map()

        # Save to cache
        try:
            with open(cache_file, 'wb') as f:
                pickle.dump(detection_map, f)
                print(f"Saved detection map to cache: {cache_file}")
        except Exception as e:
            print(f"Failed to save cache: {e}")

        return detection_map

    def _compute_fresh_detection_map(self) -> np.array:
        """Actual computation without caching"""
        lat_points = np.linspace(self.boundaries.min_lat, self.boundaries.max_lat, self.height)
        lon_points = np.linspace(self.boundaries.min_lon, self.boundaries.max_lon, self.width)

        detection_map = np.zeros((self.height, self.width), dtype=np.float32)

        for i in tqdm(range(self.height), desc="Computing detection map"):
            for j in range(self.width):
                max_possibility = 0.0
                for radar in self.radars:
                    possibility = radar.compute_detection_level(lat_points[i], lon_points[j])
                    if possibility > max_possibility:
                        max_possibility = possibility

                detection_map[i, j] = max_possibility

        # Scale with epsilon
        min_val = np.min(detection_map)
        max_val = np.max(detection_map)

        if max_val > min_val:
            detection_map = ((detection_map - min_val) / (max_val - min_val)) * (1 - EPSILON) + EPSILON
        else:
            detection_map = np.full_like(detection_map, EPSILON)

        return detection_map

    def _generate_cache_key(self) -> str:
        """Generates unique hash key for current map configuration"""
        hash_data = {
            'boundaries': (self.boundaries.min_lat, self.boundaries.max_lat,
                           self.boundaries.min_lon, self.boundaries.max_lon),
            'dimensions': (self.height, self.width),
            'radars': [(r.location.latitude, r.location.longitude) for r in self.radars],
            'params': [(r.transmission_power, r.antenna_gain, r.wavelength,
                        r.cross_section, r.minimum_signal, r.total_loss) for r in self.radars]
        }

        # Create consistent string representation
        hash_str = str(hash_data).encode('utf-8')
        return hashlib.md5(hash_str).hexdigest()

    def clear_cache(self, older_than_days: int = None):
        """Clears cache, optionally removing files older than specified days"""
        now = datetime.now()
        removed = 0

        for filename in os.listdir(self.cache_dir):
            filepath = os.path.join(self.cache_dir, filename)
            try:
                if older_than_days is not None:
                    file_time = datetime.fromtimestamp(os.path.getmtime(filepath))
                    if (now - file_time).days < older_than_days:
                        continue
                os.remove(filepath)
                removed += 1
            except Exception as e:
                print(f"Error removing {filepath}: {e}")

        print(f"Removed {removed} cache files")

    def get_cache_size(self) -> int:
        """Returns total cache size in bytes"""
        total_size = 0
        for filename in os.listdir(self.cache_dir):
            filepath = os.path.join(self.cache_dir, filename)
            total_size += os.path.getsize(filepath)
        return total_size