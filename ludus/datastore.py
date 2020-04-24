"""Datastore."""
from kafka import KafkaProducer
from configs.config import kafka_configuration


class Datastore:
    """Datastore."""

    def get_datastore(type):
        """Get datastore."""
        if type == 'kafka':
            return KafkaDatastore()


class KafkaDatastore:
    """Kakfa Datastore."""

    def __init__(self):
        """Kafka Datastore Init."""
        self.bootstrap = kafka_configuration['bootstrap_server']
        self.cacert = kafka_configuration['cacert_file']
        self.topic = kafka_configuration['topic']

        self.producer = KafkaProducer(bootstrap_servers=self.bootstrap,
                                      security_protocol='SSL',
                                      ssl_cafile=self.cacert,
                                      api_version_auto_timeout_ms=30000)

    def insert(self, json_payload):
        """Insert."""
        self.producer.send(self.topic, json_payload)
        self.producer.flush()
