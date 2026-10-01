"""
Ramer-Douglas-Peucker (RDP) trajectory compression algorithm.
"""
import math
from typing import List, Tuple

def perpendicular_distance(point: Tuple[float, float], start: Tuple[float, float], end: Tuple[float, float]) -> float:
    if start == end:
        return math.hypot(point[0] - start[0], point[1] - start[1])
    n = abs((end[0] - start[0]) * (start[1] - point[1]) - (start[0] - point[0]) * (end[1] - start[1]))
    d = math.hypot(end[0] - start[0], end[1] - start[1])
    return n / d

class PolylineSimplifier:
    @classmethod
    def simplify(cls, points: List[Tuple[float, float]], epsilon: float = 0.001) -> List[Tuple[float, float]]:
        if len(points) <= 2:
            return points

        dmax = 0.0
        index = 0
        for i in range(1, len(points) - 1):
            d = perpendicular_distance(points[i], points[0], points[-1])
            if d > dmax:
                index = i
                dmax = d

        if dmax > epsilon:
            rec_results1 = cls.simplify(points[:index + 1], epsilon)
            rec_results2 = cls.simplify(points[index:], epsilon)
            return rec_results1[:-1] + rec_results2
        else:
            return [points[0], points[-1]]
