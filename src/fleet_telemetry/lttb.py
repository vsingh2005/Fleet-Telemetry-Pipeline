"""Largest Triangle Three Buckets (LTTB) algorithm for time-series downsampling."""
from typing import List, Tuple

class LTTBDownsampler:
    @staticmethod
    def downsample(data: List[Tuple[float, float]], threshold: int) -> List[Tuple[float, float]]:
        if threshold >= len(data) or threshold <= 2:
            return data
        sampled = [data[0]]
        every = (len(data) - 2) / (threshold - 2)
        a = 0
        for i in range(threshold - 2):
            avg_x = 0.0
            avg_y = 0.0
            avg_range_start = int((i + 1) * every) + 1
            avg_range_end = min(int((i + 2) * every) + 1, len(data))
            avg_range_len = avg_range_end - avg_range_start
            for j in range(avg_range_start, avg_range_end):
                avg_x += data[j][0]
                avg_y += data[j][1]
            if avg_range_len > 0:
                avg_x /= avg_range_len
                avg_y /= avg_range_len
            range_offs = int(i * every) + 1
            range_to = min(int((i + 1) * every) + 1, len(data))
            pt_a_x, pt_a_y = data[a]
            max_area = -1.0
            next_a = range_offs
            for j in range(range_offs, range_to):
                area = abs((pt_a_x - avg_x) * (data[j][1] - pt_a_y) - (pt_a_x - data[j][0]) * (avg_y - pt_a_y)) * 0.5
                if area > max_area:
                    max_area = area
                    next_a = j
            sampled.append(data[next_a])
            a = next_a
        sampled.append(data[-1])
        return sampled
