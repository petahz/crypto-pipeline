from confluent_kafka import Producer
from krakenex import API
import json
from pykafka import KafkaClient
from pykafka.utils import serialize_utf8
from requests.exceptions import HTTPError
import time


api = API()
client = KafkaClient(zookeeper_hosts="localhost:2181")


class KrakenProducer:
    def __init__(self, asset_pair, api_method, interval=None):
        self.asset_pair = asset_pair
        self.api_method = api_method
        self.interval = interval
        self.since_time = 0

    def produce(self):
        query_params = {
            'pair': self.asset_pair,
            'since': self.since_time
        }
        if self.interval is not None:
            query_params['interval'] = self.interval
        response = api.query_public(self.api_method, query_params)

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
                    message.append(topic_name)
                    producer.produce(json.dumps(message))
                    print(topic_name, ':', message)

        return topic_name

    def produce_confluent(self):
        p = Producer({'bootstrap.servers': 'localhost'})

        def delivery_report(err, msg):
            """ Called once for each message produced to indicate delivery result.
                Triggered by poll() or flush(). """
            if err is not None:
                print('Message delivery failed: {}'.format(err))
            else:
                print('Message delivered to {} [{}] - {}'.format(msg.topic(), msg.partition(), self.asset_pair))

        query_params = {
            'pair': self.asset_pair,
            'since': self.since_time
        }
        if self.interval is not None:
            query_params['interval'] = self.interval
        try:
            response = api.query_public(self.api_method, query_params)
        except HTTPError:
            # If we get an HTTPError, wait 20 seconds and try again
            time.sleep(20)

        if len(response['error']) > 0:
            for e in response['error']:
                print('Error: ', e)
        else:
            result = response['result']

            # Set the since parameter for where in time to get the next batch of stream data from the REST API
            if getattr(result, 'last', None) is not None:
                self.since_time = result['last']

            topic_name = 'Kraken_{}'.format(self.api_method)
            if self.interval is not None:
                topic_name += '_{}'.format(self.interval)

            for data in result[self.asset_pair]:
                # Trigger any available delivery report callbacks from previous produce() calls
                p.poll(0)

                message = json.dumps(data)

                p.produce(topic_name, message.encode('utf-8'), key=self.asset_pair, callback=delivery_report)

            # Wait for any outstanding messages to be delivered and delivery report
            # callbacks to be triggered.
            p.flush()
