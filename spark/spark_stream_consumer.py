from decimal import Decimal
import json
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
import redis


KAFKA_NODES = ['ec2-52-44-121-53.compute-1.amazonaws.com:9092', 'ec2-52-22-234-28.compute-1.amazonaws.com:9092',
                 'ec2-52-45-23-147.compute-1.amazonaws.com:9092', 'ec2-18-207-65-150.compute-1.amazonaws.com:9092']

# These redis commands need to be defined outside of a class as it is passed in a dstream
r = redis.StrictRedis(host='redis-group.v7ufhi.ng.0001.use1.cache.amazonaws.com', port=6379, db=0)


def set_redis_avg_spread(partition):
    for msg in partition:
        r.hset(msg[0], 'avg_spread', msg[1])


def set_redis_bid_ask(partition):
    for msg in partition:
        r.hset(msg[3], 'bid', msg[1])
        r.hset(msg[3], 'ask', msg[2])
        r.hset(msg[3], 'spread', Decimal(msg[2]) - Decimal(msg[1]))


class SparkStreamConsumer:
    def __init__(self, slide_interval=1, window_length=5):
        self.sc = SparkContext(appName='SparkStream', master='spark://ec2-34-235-103-8.compute-1.amazonaws.com:7077')
        self.ssc = StreamingContext(self.sc, slide_interval)
        self.slide_interval = slide_interval
        self.window_length = window_length

    def start_stream(self):
        self.ssc.start()
        self.ssc.awaitTermination()

    def consume_spreads(self, spread_topics):
        self.kvs = KafkaUtils.createDirectStream(self.ssc, spread_topics,
                                                 {'metadata.broker.list': ','.join(KAFKA_NODES)})
        # messages come in [timestamp, bid, ask] format, a spread is calculated by (ask-bid)
        parsed = self.kvs.window(self.window_length, self.slide_interval).map(lambda v: json.loads(v[1])).cache()
        parsed.foreachRDD(lambda rdd: rdd.foreachPartition(set_redis_bid_ask))

        def calculate_spread(tx):
            asset_pair = tx[3]
            return (asset_pair, Decimal(tx[2]) - Decimal(tx[1]))

        spread_percentage_dstream = parsed.map(calculate_spread).mapValues(lambda x: (x, 1))

        spread_sum_count_dstream = spread_percentage_dstream.reduceByKey(lambda x, y: (x[0] + y[0], x[1] + y[1]))

        average_spread_dstream = spread_sum_count_dstream.mapValues(lambda x: x[0] / x[1])

        average_spread_dstream.pprint()

        average_spread_dstream.foreachRDD(lambda rdd: rdd.foreachPartition(set_redis_avg_spread))
