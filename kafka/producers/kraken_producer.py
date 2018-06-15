from krakenex import API
import json
from pykafka import KafkaClient
from pykafka.utils import serialize_utf8


api = API()
client = KafkaClient(zookeeper_hosts="localhost:2181")


class Producer:
    def __init__(self, asset_pair, api_method):
        self.asset_pair = asset_pair
        self.api_method = api_method
        self.since_time = 0

    def produce(self):
        response = api.query_public(self.api_method, {
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

            topic_name = '{}_{}'.format(self.asset_pair, self.api_method)
            topic = client.topics[topic_name]

            with topic.get_producer(delivery_reports=False, serializer=serialize_utf8) as producer:
                messages = result[self.asset_pair]
                for message in messages:
                    producer.produce(json.dumps(message))
                    print(topic_name, ':', message)

        return topic_name
