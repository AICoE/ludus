"""Validator."""

from configs import event_configuration
from jsonschema import ValidationError
from jsonschema import validate


class Validator:
    """Validator."""

    def get_validator(event_source):
        """Get validator."""
        if event_source == "default":
            return DefaultEventValidator()


class DefaultEventValidator:
    """Default event validator."""

    def get_valid_event_types(self, event):
        """Get valid event names."""
        valid_event_types = list()

        for event_type in event_configuration.config.keys():
            try:
                schema = event_configuration.config[event_type]['validator']
                validate(instance=event, schema=schema)
                valid_event_types.append(event_type)
            except ValidationError as ve:
                continue

        return valid_event_types
