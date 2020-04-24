"""Review validator."""
schema = {
    "type": "object",
    "properties": {
        "action": {
            "type": "string",
            "pattern": "closed"
        },
        "pull_request": {
            "type": "object",
            "properties": {
                "merged": {"enum": [True]}
            },
            "required": ["merged"]
        }
    },
    "required": ["action", "pull_request"]
}
