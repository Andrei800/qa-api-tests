# tests/schemas/user.py

user_schema = {
    "type": "object",
    "required": ["id", "name", "email", "gender", "status"],
    "properties": {
        "id":     {"type": "integer"},
        "name":   {"type": "string", "minLength": 1},
        "email":  {"type": "string", "format": "email"},
        "gender": {"type": "string", "enum": ["male", "female"]},
        "status": {"type": "string", "enum": ["active", "inactive"]},
    },
    "additionalProperties": True  # сервис может присылать ещё поля
}

users_list_schema = {
    "type": "array",
    "items": user_schema
}