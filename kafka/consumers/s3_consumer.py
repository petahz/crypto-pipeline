import boto3
from confluent_kafka import Consumer, KafkaError
import datetime
import json
from pykafka import KafkaClient


kf_client = KafkaClient(hosts="localhost:9092")
s3 = boto3.client('s3')


class S3Consumer:
    def __init__(self, bucket_name):
        self.bucket_name = bucket_name

    def consume(self, topic_name):
        exchange, method = topic_name.decode().split('_')

        topic = kf_client.topics[topic_name]
        consumer = topic.get_simple_consumer()
        current_ts = 0
        body_content = []

        for message in consumer:
            if message is not None:
                asset_pair = message.partition_key.decode()
                content = json.loads(message.value.decode())
                body_content.append(content)
                timestamp = content[0]
                dt_attr = datetime.datetime.utcfromtimestamp(timestamp)
                key = '{0}/{1}/{2}/{3}/{4}/{5}/{6}'.format(exchange, asset_pair, method, dt_attr.year, dt_attr.month,
                                                       dt_attr.day, timestamp)

                if current_ts != timestamp:
                    current_ts = timestamp
                    s3.put_object(Body=json.dumps(body_content), Bucket=self.bucket_name, Key=key)
                    body_content = []

                print(message.offset, asset_pair, content)

    def consume_confluent(self):
        c = Consumer({
            'bootstrap.servers': 'localhost',
            'group.id': 's3',
            'default.topic.config': {
                'auto.offset.reset': 'smallest'
            }
        })

        topics = [topic.decode() for topic in kf_client.topics]
        c.subscribe(topics)

        body_content = []
        current_key = ''
        while True:
            msg = c.poll(1.0)

            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                else:
                    print(msg.error())
                    break

            topic_name = msg.topic()
            exchange, method = topic_name.split('_')

            asset_pair = msg.key().decode()
            content = json.loads(msg.value().decode())
            body_content.append(content)
            timestamp = content[0]
            dt_attr = datetime.datetime.utcfromtimestamp(timestamp)
            key = '{0}/{1}/{2}/{3}/{4}/{5}/{6}'.format(exchange, asset_pair, method, dt_attr.year, dt_attr.month,
                                                       dt_attr.day, timestamp)

            if current_key != key:
                s3.put_object(Body=json.dumps(body_content), Bucket=self.bucket_name, Key=key)
                current_key = key
                body_content = []

            print('Received message: {}'.format(msg.value().decode('utf-8')))

        c.close()

if __name__ == '__main__':
    # We want to store all data coming in Kafka to S3
    S3Consumer(bucket_name='crypto-pipeline').consume_confluent()
