from pykafka import KafkaClient


client = KafkaClient(hosts="ec2-52-44-121-53.compute-1.amazonaws.com:9092")


class Consumer:
    def __init__(self, asset_pair):
        self.asset_pair = asset_pair

    def consume(self, method):
        topic_name = '{}_{}'.format(self.asset_pair, method)
        topic = client.topics[topic_name.encode()]
        consumer = topic.get_simple_consumer()

        for message in consumer:
            if message is not None:
                print(message.offset, message.value)
