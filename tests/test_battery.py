from fleet_telemetry.battery import BatterySoCEstimator

def test_soc_coulomb_integration():
    batt = BatterySoCEstimator(nominal_capacity_ah=100.0, initial_soc=1.0)
    soc = batt.integrate(current_amps=50.0, dt_seconds=3600.0)
    assert abs(soc - 0.5) < 1e-3
    est_range = batt.estimate_remaining_range(avg_consumption_kwh_per_km=0.2, pack_voltage=400.0)
    assert est_range == 100.0
