"""Trello commend validator."""
schema = {
    "type": "object",
    "properties": {
        "action": {
            "type": "object",
            "properties": {
                "type": {
                    "type": "string",
                    "pattern": "commentCard"
                }
            },
            "required": ["type"]
        }
    },
    "required": ["action"]
}
