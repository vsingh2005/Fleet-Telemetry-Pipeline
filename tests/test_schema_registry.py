from fleet_telemetry.schema_registry import SchemaValidator

def test_schema_backward_compatibility():
    old_s = {"id": "string", "speed": "float"}
    new_s = {"id": "string", "speed": "float", "fuel": "float"}
    assert SchemaValidator.is_backward_compatible(old_s, new_s) is True

    incompatible = {"id": "string"}
    assert SchemaValidator.is_backward_compatible(old_s, incompatible) is False
