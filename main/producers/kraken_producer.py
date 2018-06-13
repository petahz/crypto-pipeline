from krakenex import API
from pykafka import KafkaClient


api = API()
client = KafkaClient(hosts="ec2-52-44-121-53.compute-1.amazonaws.com:9092")


class Producer:
    def __init__(self, asset_pair):
        self.asset_pair = asset_pair
        self.since_time = 0

    def produce(self, method):
        response = api.query_public(method, {
            'pair': self.asset_pair,
            'since': self.since_time
        })

        # Set the since parameter for where in time to get the next batch of stream data from the REST API
        self.since_time = response['last']

        topic = client.topics['{}_{}'.format(self.asset_pair, method)]

        with topic.get_producer(delivery_reports=False) as producer:
            producer.produce(response)
