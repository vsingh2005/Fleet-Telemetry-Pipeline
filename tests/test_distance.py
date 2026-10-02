import numpy as np
from fleet_telemetry.distance import HaversineMatrix

def test_haversine_matrix():
    coords = np.array([
        [42.3601, -71.0589],
        [40.7128, -74.0060],
        [42.3601, -71.0589],
    ])
    matrix = HaversineMatrix.pairwise_distance(coords)
    assert matrix.shape == (3, 3)
    assert matrix[0, 0] == 0.0
    assert matrix[0, 2] == 0.0
    assert 300 < matrix[0, 1] < 360
