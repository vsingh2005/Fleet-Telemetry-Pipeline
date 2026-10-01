from fleet_telemetry.simplifier import PolylineSimplifier

def test_rdp_simplification():
    points = [(0.0, 0.0), (1.0, 0.0001), (2.0, -0.0001), (3.0, 0.0), (4.0, 1.0)]
    simplified = PolylineSimplifier.simplify(points, epsilon=0.01)
    assert len(simplified) < len(points)
    assert simplified[0] == (0.0, 0.0)
    assert simplified[-1] == (4.0, 1.0)
