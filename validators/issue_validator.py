"""Issue validator."""
schema = {
    "type": "object",
    "properties": {
        "action": {
            "type": "string",
            "pattern": "opened"
        },
        "issue": {
            "type": "object",
        }
    },
    "required": ["action", "issue"]
}
