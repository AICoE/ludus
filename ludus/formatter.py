"""Formatter."""
from configs import event_configuration
from configs import config
import datetime
import json
from formatters.processor import Processor


class Formatter:
    """Formatter."""

    def get_formatter(type):
        """Get formatter."""
        if type == 'default':
            return DefaultEventFormatter()


class DefaultEventFormatter:
    """Default event formatter."""

    def format(self, event, event_type):
        """Format."""
        event_formatter = event_configuration.config[event_type]['formatter']
        jinja_environment = config.formatter_configuration['jinja_environment']
        event_processor = Processor.get_processor(event_type)
        formatted_event = jinja_environment.get_template(event_formatter).render(event=event,
                                                                                 timestamp=datetime.datetime.now()
                                                                                 .strftime("%Y-%m-%d %H:%M:%S"),
                                                                                 variables=event_processor
                                                                                 .get_variables(event_type, event),
                                                                                 json_event=json.dumps(event))
        formatted_event = json.loads(formatted_event)
        return formatted_event
