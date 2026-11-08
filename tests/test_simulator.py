from fleet_telemetry.simulator import TripSimulator

def test_trip_simulator():
    steps = list(TripSimulator.generate_trip(duration_steps=20))
    assert len(steps) == 20
    assert 0 <= steps[0]["speed"] <= 120
    assert steps[0]["rpm"] > 0
