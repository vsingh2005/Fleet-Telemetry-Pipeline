from fleet_telemetry.lttb import LTTBDownsampler

def test_lttb_downsampling():
    raw = [(float(i), float(i ** 2)) for i in range(50)]
    sampled = LTTBDownsampler.downsample(raw, 10)
    assert len(sampled) == 10
    assert sampled[0] == raw[0]
    assert sampled[-1] == raw[-1]
