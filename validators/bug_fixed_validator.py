"""Bug fix validator."""
schema = {
    "type": "object",
    "properties": {
        "action": {
            "type": "string",
            "pattern": "closed"
        },
        "issue": {
            "type": "object",
            "properties": {
                "labels": {
                    "type": "array",
                    "contains": {
                        "type": "object",
                        "properties": {
                            "name": {
                                "type": "string",
                                "pattern": "bug"
                            }
                        },
                        "required": ["name"]
                    }
                }
            },
            "required": ["labels"]
        }
    },
    "required": ["action", "issue"]
}
