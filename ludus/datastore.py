from kafka import KafkaProducer
from configs.config import kafka_configuration

class Datastore:
    def get_datastore(type):
        if type == 'kafka':
            return KafkaDatastore()

class KafkaDatastore:

    def __init__(self):
        self.bootstrap = kafka_configuration['bootstrap_server']
        self.cacert = kafka_configuration['cacert_file']
        self.topic = kafka_configuration['topic']

        self.producer = KafkaProducer(bootstrap_servers=self.bootstrap,
                                        security_protocol='SSL',
                                        ssl_cafile=self.cacert,
                                        api_version_auto_timeout_ms=30000)


    def insert(self, json_payload):
        self.producer.send(self.topic, json_payload)
        self.producer.flush()