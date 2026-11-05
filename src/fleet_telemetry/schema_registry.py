"""
Schema compatibility validator checking backward and forward compatibility.
"""
from typing import Dict, Any, List

class SchemaValidator:
    @staticmethod
    def is_backward_compatible(old_schema: Dict[str, str], new_schema: Dict[str, str]) -> bool:
        for field, f_type in old_schema.items():
            if field not in new_schema:
                return False
            if new_schema[field] != f_type:
                return False
        return True

    @staticmethod
    def validate_record(record: Dict[str, Any], schema: Dict[str, str]) -> List[str]:
        errors = []
        for field, expected_type in schema.items():
            if field not in record:
                errors.append(f"Missing field: {field}")
            else:
                val = record[field]
                if expected_type == "int" and not isinstance(val, int):
                    errors.append(f"Field {field} expected int, got {type(val).__name__}")
                elif expected_type == "float" and not isinstance(val, (float, int)):
                    errors.append(f"Field {field} expected float, got {type(val).__name__}")
                elif expected_type == "string" and not isinstance(val, str):
                    errors.append(f"Field {field} expected string, got {type(val).__name__}")
        return errors
