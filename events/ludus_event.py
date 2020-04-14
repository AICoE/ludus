"""Ludus events."""
from datetime import datetime
import faust
import json


class LudusEvent(faust.Record, isodates=True, serializer="json"):
    """Ludus event."""

    username: str = None
    type: str = None
    timestamp: datetime = None
    event_source: str = None
    event_url: str = None
    event_type: str = None
    raw_github: json = None
    raw_trello: json = None
    issue_closes: str = None
