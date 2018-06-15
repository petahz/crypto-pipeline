from config.config import KAFKA_NODES

import json

from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils


class SparkStreamConsumer:
    spark_context = None

    def __init__(self, topic_name):
        self.topic_name = topic_name

        self.sc = SparkContext(appName=self.spark_context)
        self.ssc = StreamingContext(self.sc, 5)

        self.kvs = KafkaUtils.createDirectStream(self.ssc, [self.topic_name.encode()],
                                                 {'metadata.broker.list': KAFKA_NODES})

    def consume(self):
        self.ssc.start()
        self.ssc.awaitTermination()


class AverageSpreadConsumer(SparkStreamConsumer):
    spark_context = 'AverageSpread'

    def __init__(self, topic_name):
        super().__init__(topic_name)

    def consume(self):
        # messages come in [timestamp, bid, ask] format, a spread is calculated by (ask-bid)
        parsed = self.kvs.map(lambda v: json.loads(v[1]))
        spreads_dstream = parsed.map(lambda tx: [tx[0], tx[2] - tx[1]])
        spreads_dstream.pprint()

        super().consume()
