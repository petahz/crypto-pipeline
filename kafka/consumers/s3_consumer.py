import boto3
from datetime import datetime
import json
from pykafka import KafkaClient


kf_client = KafkaClient(hosts="localhost:9092")
s3 = boto3.client('s3')


class S3Consumer:
    def __init__(self, bucket_name):
        self.bucket_name = bucket_name

    def consume(self):
        # We want to store all data coming in Kafka to S3
        for topic in kf_client.topics:
            asset_pair, method = topic.split('_')
            consumer = topic.get_simple_consumer()
            current_ts = 0
            body_content = []

            for message in consumer:
                if message is not None:
                    content = json.loads(message.value.decode())
                    body_content.append(content)
                    timestamp = content[0]
                    dt_attr = datetime.datetime(timestamp)
                    key = '{0}/{1}/{2}/{3}/{4}/{5}'.format(asset_pair, method, dt_attr.year, dt_attr.month,
                                                           dt_attr.day, timestamp)

                    if current_ts != timestamp:
                        current_ts = timestamp
                        s3.put_object(Body=json.dumps(body_content), Bucket=self.bucket_name, Key=key)
                        body_content = []

                    print(message.offset, message.value)


if __name__ == '__main__':
    S3Consumer(bucket_name='crypto-pipeline').consume()