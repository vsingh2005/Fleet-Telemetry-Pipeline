from fleet_telemetry.thermal import ThermalTrendPredictor

def test_thermal_prediction():
    predictor = ThermalTrendPredictor(warning_temp=100.0)
    for t in [85.0, 88.0, 92.0, 96.0, 100.0]:
        res = predictor.update(t)
    assert res["throttle_warning"] is True
    assert res["estimated_trend"] > 0

def test_cool_temperature_does_not_warn():
    assert ThermalTrendPredictor().update(25.0)["throttle_warning"] is False
