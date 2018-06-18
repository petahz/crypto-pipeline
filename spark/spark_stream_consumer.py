from datetime import timedelta
from decimal import Decimal
import json
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
import time

KAFKA_NODES = ['ec2-52-44-121-53.compute-1.amazonaws.com:9092', 'ec2-52-22-234-28.compute-1.amazonaws.com:9092',
                 'ec2-52-45-23-147.compute-1.amazonaws.com:9092', 'ec2-18-207-65-150.compute-1.amazonaws.com:9092']


class SparkStreamConsumer:
    spark_context = None

    def __init__(self, topic_name):
        self.topic_name = topic_name

        self.sc = SparkContext(appName=self.spark_context)
        self.ssc = StreamingContext(self.sc, 5)

        self.kvs = KafkaUtils.createDirectStream(self.ssc, [self.topic_name],
                                                 {'metadata.broker.list': 'localhost:9092'})

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

        # Filter to spreads in the last 5 seconds
        def last_five_seconds(sp):
            five_seconds_ago = time.time() - timedelta(seconds=5).total_seconds()
            return sp[0] > five_seconds_ago

        recent_spreads_dstream = parsed.filter(last_five_seconds)

        # We use a percentage for a fairer comparison of spread than just the difference
        # Spread % = 2 x (Ask – Bid) / (Ask + Bid) x 100 %
        def spread_percentage(tx):
            return 2 * (Decimal(tx[2]) - Decimal(tx[1])) / ((Decimal(tx[2]) + Decimal(tx[1])) * 100)

        spread_percentage_dstream = recent_spreads_dstream.map(spread_percentage)

        count = spread_percentage_dstream.count()

        count.pprint()

        # sum_spread_dstream = spread_percentage_dstream.reduce(lambda x,y: x + y)
        #
        # average_spread_dstream = sum_spread_dstream.map(lambda sum: sum / count)
        #
        # average_spread_dstream.pprint()

        super().consume()
