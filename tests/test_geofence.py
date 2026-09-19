from fleet_telemetry.geofence import GeofenceValidator

def test_haversine_and_geofence_circle():
    nyc_lat, nyc_lon = 40.7128, -74.0060
    point_lat, point_lon = 40.7130, -74.0065
    inside = GeofenceValidator.is_inside_circle(point_lat, point_lon, nyc_lat, nyc_lon, radius_km=1.0)
    assert inside is True
    outside = GeofenceValidator.is_inside_circle(41.0, -74.0, nyc_lat, nyc_lon, radius_km=1.0)
    assert outside is False

def test_geofence_polygon():
    square = [(0.0, 0.0), (0.0, 10.0), (10.0, 10.0), (10.0, 0.0)]
    assert GeofenceValidator.is_inside_polygon(5.0, 5.0, square) is True
    assert GeofenceValidator.is_inside_polygon(15.0, 5.0, square) is False
