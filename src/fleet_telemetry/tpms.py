"""
TPMS pressure-temperature correlation checker.
"""
class TPMSValidator:
    def __init__(self, target_cold_psi: float = 32.0, cold_temp_c: float = 20.0):
        self.target_cold_psi = target_cold_psi
        self.cold_temp_k = cold_temp_c + 273.15

    def normalize_pressure(self, measured_psi: float, measured_temp_c: float) -> float:
        temp_k = measured_temp_c + 273.15
        if temp_k <= 0:
            return measured_psi
        normalized_psi = measured_psi * (self.cold_temp_k / temp_k)
        return round(normalized_psi, 1)

    def diagnose_tire(self, measured_psi: float, measured_temp_c: float) -> dict:
        norm = self.normalize_pressure(measured_psi, measured_temp_c)
        ratio = norm / self.target_cold_psi
        status = "nominal"
        if ratio < 0.75:
            status = "severe_underinflation"
        elif ratio < 0.88:
            status = "underinflation"
        elif ratio > 1.20:
            status = "overinflation"
            
        return {
            "measured_psi": measured_psi,
            "normalized_psi": norm,
            "status": status,
            "alert": status != "nominal"
        }
