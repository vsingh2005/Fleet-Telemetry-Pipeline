from fleet_telemetry.watermark import BoundedWatermarkGenerator

def test_watermark_late_events():
    gen = BoundedWatermarkGenerator(max_out_of_orderness_seconds=5.0)
    wm1, is_late1 = gen.on_event(100.0)
    assert wm1 == 95.0
    assert is_late1 is False

    wm2, is_late2 = gen.on_event(97.0)
    assert is_late2 is False

    wm3, is_late3 = gen.on_event(92.0)
    assert is_late3 is True
