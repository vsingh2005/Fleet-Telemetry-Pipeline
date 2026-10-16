"""
EV battery State of Charge (SoC) Coulomb counter and health estimator.
"""
class BatterySoCEstimator:
    def __init__(self, nominal_capacity_ah: float, initial_soc: float = 1.0):
        self.nominal_capacity_ah = nominal_capacity_ah
        self.soc = float(initial_soc)

    def integrate(self, current_amps: float, dt_seconds: float) -> float:
        delta_ah = (current_amps * dt_seconds) / 3600.0
        delta_soc = delta_ah / self.nominal_capacity_ah
        self.soc = max(0.0, min(1.0, self.soc - delta_soc))
        return round(self.soc, 4)

    def estimate_remaining_range(self, avg_consumption_kwh_per_km: float, pack_voltage: float = 400.0) -> float:
        remaining_kwh = (self.soc * self.nominal_capacity_ah * pack_voltage) / 1000.0
        if avg_consumption_kwh_per_km <= 0.0:
            return 0.0
        return round(remaining_kwh / avg_consumption_kwh_per_km, 1)
