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

        if len(response['error']) > 0:
            for e in response['error']:
                print('Error: ', e)
        else:
            result = response['result']

            # Set the since parameter for where in time to get the next batch of stream data from the REST API
            self.since_time = result['last']

            topic = client.topics['{}_{}'.format(self.asset_pair, method)]

            with topic.get_producer(delivery_reports=False) as producer:
                message = result[self.asset_pair]
                producer.produce(message)
