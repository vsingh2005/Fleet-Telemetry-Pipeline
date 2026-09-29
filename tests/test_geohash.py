from fleet_telemetry.geohash import GeohashIndex

def test_geohash_encoding():
    gh = GeohashIndex.encode(42.3601, -71.0589, precision=6)
    assert isinstance(gh, str)
    assert len(gh) == 6
    assert gh.startswith("drt")
