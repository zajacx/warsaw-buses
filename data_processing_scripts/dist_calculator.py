import numpy as np


def calculate_distance(position1, position2):
    earth_r = 6371000.0
    lon1, lat1 = position1
    lon2, lat2 = position2
    lat1, lon1 = np.radians(lat1), np.radians(lon1)
    lat2, lon2 = np.radians(lat2), np.radians(lon2)
    lon_diff = lon2 - lon1
    lat_diff = lat2 - lat1

    a = np.sin(lat_diff / 2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(lon_diff / 2)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))

    return earth_r * c
