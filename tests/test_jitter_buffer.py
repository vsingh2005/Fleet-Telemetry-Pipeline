from fleet_telemetry.jitter_buffer import PacketJitterBuffer

def test_jitter_buffer_reordering():
    jb = PacketJitterBuffer()
    assert jb.insert(1, "pkg_1") == []
    assert jb.insert(0, "pkg_0") == ["pkg_0", "pkg_1"]
    assert jb.insert(2, "pkg_2") == ["pkg_2"]
