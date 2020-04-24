"""Task completed validator."""
schema = {
    "type": "object",
    "properties": {
        "action": {
            "type": "object",
            "properties": {
                "type": {
                    "type": "string",
                    "pattern": "updateCard"
                },
                "data": {
                    "type": "object",
                    "properties": {
                        "listAfter": {
                            "type": "object",
                            "properties": {
                                "name": {
                                    "type": "string",
                                    "pattern": "Completed"
                                }
                            },
                            "required": ["name"]
                        }
                    },
                    "required": ["listAfter"]
                }
            },
            "required": ["type", "data"]
        }
    },
    "required": ["action"]
}
