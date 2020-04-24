"""Task moved to backlog validator."""
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
                                    "pattern": "Backlog"
                                }
                            },
                            "required": ["name"]
                        },
                        "listBefore": {
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
                    "required": ["listAfter", "listBefore"]
                }
            },
            "required": ["type", "data"]
        }
    },
    "required": ["action"]
}
