from decimal import Decimal
import json
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
import redis

from config.config import KAFKA_NODES


r = redis.StrictRedis(host='redis-group.v7ufhi.ng.0001.use1.cache.amazonaws.com', port=6379, db=0)

# This needs to be defined outside of a class as it is passed in a dstream
def set_redis(partition):
    for msg in partition:
        r.set(msg[0], msg[1])


class SparkStreamConsumer:
    spark_context = None

    def __init__(self, slide_interval=1, window_length=5):
        self.sc = SparkContext(appName=self.spark_context)
        self.ssc = StreamingContext(self.sc, slide_interval)
        self.slide_interval = slide_interval
        self.window_length = window_length

    def consume(self):
        self.ssc.start()
        self.ssc.awaitTermination()


class AverageSpreadStreamConsumer(SparkStreamConsumer):
    spark_context = 'AverageSpread'

    def __init__(self, slide_interval=1, window_length=5):
        super().__init__(slide_interval, window_length)

    def consume(self, topics):
        self.kvs = KafkaUtils.createDirectStream(self.ssc, topics,
                                                 {'metadata.broker.list': KAFKA_NODES.join('')})

        # messages come in [timestamp, bid, ask] format, a spread is calculated by (ask-bid)
        parsed = self.kvs.window(self.window_length, self.slide_interval).map(lambda v: json.loads(v[1]))

        def calculate_spread(tx):
            asset_pair = tx[3]
            return (asset_pair, Decimal(tx[2]) - Decimal(tx[1]))

        spread_percentage_dstream = parsed.map(calculate_spread).mapValues(lambda x: (x, 1))

        spread_sum_count_dstream = spread_percentage_dstream.reduceByKey(lambda x, y: (x[0]+y[0], x[1]+y[1]))

        average_spread_dstream = spread_sum_count_dstream.mapValues(lambda x: x[0] / x[1])

        average_spread_dstream.foreachRDD(lambda rdd: rdd.foreachPartition(set_redis))

        super().consume()


class FinancialMetricStreamConsumer(SparkStreamConsumer):
    spark_context = 'FinancialMetrics'

    def __init__(self):
        super().__init__()

    def consume(self, topics):
        self.kvs = KafkaUtils.createDirectStream(self.ssc, topics,
                                                 {'metadata.broker.list': KAFKA_NODES.join('')})

        # messages come in [timestamp, open, high, low, close, vwap, volume, count] format
        parsed = self.kvs.map(lambda v: json.loads(v[1]))

        def calculate_rsi(tx):
            asset_pair = tx[3]
            return (asset_pair, Decimal(tx[2]) - Decimal(tx[1]))

        spread_percentage_dstream = parsed.map(calculate_spread).mapValues(lambda x: (x, 1))

        spread_sum_count_dstream = spread_percentage_dstream.reduceByKey(lambda x, y: (x[0]+y[0], x[1]+y[1]))

        average_spread_dstream = spread_sum_count_dstream.mapValues(lambda x: x[0] / x[1])

        average_spread_dstream.foreachRDD(lambda rdd: rdd.foreachPartition(set_redis))

        super().consume()
