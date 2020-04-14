"""Issue closed validator."""
schema = {
    "type": "object",
    "properties": {
        "action": {
            "type": "string",
            "pattern": "closed"
        },
        "issue": {
            "type": "object",
        }
    },
    "required": ["action", "issue"]
}
