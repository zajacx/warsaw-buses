import numpy as np


def calculate_distance(position1, position2):
    earth_r = 6371000.0
    lon1 = np.radians(position1[0])
    lat1 = np.radians(position1[1])
    lon2 = np.radians(position2[0])
    lat2 = np.radians(position2[1])
    a = np.sin(lat2 - lat1 / 2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(lon2 - lon1 / 2)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    return earth_r * c
