import pytest
from fleet_telemetry.tpms import TPMSValidator

def test_tpms_normalization():
    tpms = TPMSValidator(target_cold_psi=35.0, cold_temp_c=20.0)
    diag = tpms.diagnose_tire(measured_psi=26.0, measured_temp_c=45.0)
    assert diag["normalized_psi"] == 24.0
    assert diag["alert"] is True
    # 24 / 35 is below the severe underinflation threshold of 75%.
    assert diag["status"] == "severe_underinflation"

@pytest.mark.parametrize("pressure,status", [
    (74.9, "severe_underinflation"),
    (75.0, "underinflation"),
    (87.9, "underinflation"),
    (88.0, "nominal"),
    (120.0, "nominal"),
    (120.1, "overinflation"),
])
def test_tpms_warning_thresholds(pressure, status):
    tpms = TPMSValidator(target_cold_psi=100.0, cold_temp_c=20.0)
    diag = tpms.diagnose_tire(measured_psi=pressure, measured_temp_c=20.0)
    assert diag["normalized_psi"] == pressure
    assert diag["status"] == status
    assert diag["alert"] is (status != "nominal")
