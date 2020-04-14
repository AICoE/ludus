"""Schema for new idea validator."""
schema = {
    "type": "object",
    "properties": {
        "action": {
            "type": "object",
            "properties": {
                "type": {
                    "type": "string",
                    "pattern": "createCard"
                },
                "data": {
                    "type": "object",
                    "properties": {
                        "list": {
                            "type": "object",
                            "properties": {
                                "name": {
                                    "type": "string",
                                    "pattern": "New"
                                }
                            },
                            "required": ["name"]
                        }
                    },
                    "required": ["list"]
                }
            },
            "required": ["type", "data"]
        }
    },
    "required": ["action"]
}
