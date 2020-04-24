"""Main configuration file for the application."""
from jinja2 import Environment, FileSystemLoader
import os

datastore_configuration = {
    'type': 'kafka'
}

kafka_configuration = {
    'bootstrap_server': os.environ['kafka_bootstrap_server'],
    'cacert_file': 'resources/data-hub-kafka-ca.crt',
    'topic': os.environ['kafka_topic']
}

awarder_configuration = {
    'faust_app_name': os.environ['awarder_name'],
    'faust_store': 'memory://',
    'events_table_name': os.environ['events_table_name'],
    'badges_table_name': os.environ['badges_table_name'],
    'port': int(os.environ['awarder_port'])
}

formatter_configuration = {
    'jinja_environment': Environment(loader=FileSystemLoader('formatters'))
}
