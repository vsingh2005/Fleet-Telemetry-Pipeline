from typing import List

class DeltaEncoder:
    @staticmethod
    def encode(values: List[int]) -> List[int]:
        if not values:
            return []
        if len(values) == 1:
            return [values[0]]
        deltas = [values[0], values[1] - values[0]]
        for i in range(2, len(values)):
            d1 = values[i] - values[i - 1]
            d0 = values[i - 1] - values[i - 2]
            deltas.append(d1 - d0)
        return deltas

    @staticmethod
    def decode(deltas: List[int]) -> List[int]:
        if not deltas:
            return []
        if len(deltas) == 1:
            return [deltas[0]]
        values = [deltas[0], deltas[0] + deltas[1]]
        cur_d = deltas[1]
        for dod in deltas[2:]:
            cur_d += dod
            values.append(values[-1] + cur_d)
        return values
