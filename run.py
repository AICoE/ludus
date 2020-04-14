"""Run."""

from configs.config import datastore_configuration
from http import HTTPStatus
from flask import Flask, Response, request
from ludus.formatter import Formatter
from ludus.validator import Validator
from ludus.datastore import Datastore
import json

# constants
EVENT_SOURCE_GITHUB = "github"
EVENT_SOURCE_TRELLO = "trello"
STATUS_CODE_200 = HTTPStatus.OK
STATUS_CODE_500 = HTTPStatus.INTERNAL_SERVER_ERROR

# initializing datastore
datastore = Datastore.get_datastore(datastore_configuration['type'])

app = Flask(__name__)


@app.route('/', methods=['POST', 'HEAD'])
def ludus_event():
    """Func Ludus event."""
    resp = Response()
    event = request.json

    validator = Validator.get_validator('default')
    event_types = validator.get_valid_event_types(event)

    for event_type in event_types:
        formatter = Formatter.get_formatter('default')
        formatted_event = formatter.format(event, event_type)
        formatted_event_json = json.dumps(formatted_event)

        try:
            datastore.insert(formatted_event_json.encode('utf-8'))
        except Exception as e:
            resp.status = "failed to insert event into datastore: " + str(e)
            return resp, STATUS_CODE_500

    resp.status = "successfuly inserted event into datastore"
    return resp, STATUS_CODE_200


if __name__ == "__main__":
    """Main method."""
    app.run(host='0.0.0.0', port=5000)
