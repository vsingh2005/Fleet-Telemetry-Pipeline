from fleet_telemetry.spatial_tree import SpatialKDTree

def test_kdtree_nearest_vehicle():
    fleet = [
        ((42.35, -71.06), "truck_1"),
        ((40.71, -74.00), "truck_2"),
        ((42.38, -71.10), "truck_3"),
    ]
    tree = SpatialKDTree(fleet)
    veh, dist = tree.nearest((42.36, -71.07))
    assert veh == "truck_1"
