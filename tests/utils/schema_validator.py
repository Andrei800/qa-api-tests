# tests/utils/schema_validator.py
from jsonschema import Draft7Validator, FormatChecker

format_checker = FormatChecker()

def assert_schema(instance, schema, *, name: str = "response"):
    """
    Валидирует JSON 'instance' по 'schema'.
    В случае ошибки бросает AssertionError с понятным путём к полю.
    """
    validator = Draft7Validator(schema, format_checker=format_checker)
    errors = sorted(validator.iter_errors(instance), key=lambda e: e.path)
    if not errors:
        return

    lines = [f"[{name}] JSON Schema validation failed ({len(errors)} error(s)):"]
    for err in errors:
        path = "$" + "".join(f".{p}" if isinstance(p, str) else f"[{p}]" for p in err.path)
        lines.append(f"- {path}: {err.message}")
    raise AssertionError("\n".join(lines))
