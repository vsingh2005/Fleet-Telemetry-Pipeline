"""
Thermal runaway trend detector using Holt's linear exponential smoothing.
"""
class ThermalTrendPredictor:
    def __init__(self, alpha: float = 0.3, beta: float = 0.1, warning_temp: float = 105.0):
        self.alpha = alpha
        self.beta = beta
        self.warning_temp = warning_temp
        self.level = None
        self.trend = 0.0

    def update(self, temp: float) -> dict:
        if self.level is None:
            self.level = temp
            self.trend = 0.0
        else:
            prev_level = self.level
            self.level = self.alpha * temp + (1 - self.alpha) * (self.level + self.trend)
            self.trend = self.beta * (self.level - prev_level) + (1 - self.beta) * self.trend

        forecast_60s = self.level + (self.trend * 6.0)
        return {
            "current_temp": temp,
            "estimated_trend": round(self.trend, 3),
            "forecast_60s": round(forecast_60s, 2),
            "throttle_warning": temp >= self.warning_temp or forecast_60s >= self.warning_temp
        }
