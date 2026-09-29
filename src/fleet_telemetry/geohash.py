"""
Base32 Geohash encoder and spatial proximity query utility.
"""
from typing import Tuple

BASE32 = "0123456789bcdefghjkmnpqrstuvwxyz"

class GeohashIndex:
    @staticmethod
    def encode(lat: float, lon: float, precision: int = 7) -> str:
        lat_interval = [-90.0, 90.0]
        lon_interval = [-180.0, 180.0]
        geohash = []
        bits = [16, 8, 4, 2, 1]
        bit = 0
        ch = 0
        is_even = True

        while len(geohash) < precision:
            if is_even:
                mid = (lon_interval[0] + lon_interval[1]) / 2.0
                if lon > mid:
                    ch |= bits[bit]
                    lon_interval[0] = mid
                else:
                    lon_interval[1] = mid
            else:
                mid = (lat_interval[0] + lat_interval[1]) / 2.0
                if lat > mid:
                    ch |= bits[bit]
                    lat_interval[0] = mid
                else:
                    lat_interval[1] = mid
            is_even = not is_even
            if bit < 4:
                bit += 1
            else:
                geohash.append(BASE32[ch])
                bit = 0
                ch = 0
        return "".join(geohash)
