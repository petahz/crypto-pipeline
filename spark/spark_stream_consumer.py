from decimal import Decimal
import json
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
import redis

from config.config import KAFKA_NODES

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
                                                 {'metadata.broker.list': 'localhost:9092'})
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

    def consume_ohlc(self, ohlc_topics):
        self.kvs = KafkaUtils.createDirectStream(self.ssc, ohlc_topics,
                                                 {'metadata.broker.list': KAFKA_NODES.join('')})

        # messages come in [timestamp, open, high, low, close, vwap, volume, count] format
        parsed = self.kvs.map(lambda v: json.loads(v[1]))

        def calculate_rsi(tx):
            asset_pair = tx[3]
            return (asset_pair, Decimal(tx[2]) - Decimal(tx[1]))

        spread_percentage_dstream = parsed.map(calculate_rsi).mapValues(lambda x: (x, 1))

        spread_sum_count_dstream = spread_percentage_dstream.reduceByKey(lambda x, y: (x[0] + y[0], x[1] + y[1]))

        average_spread_dstream = spread_sum_count_dstream.mapValues(lambda x: x[0] / x[1])

        average_spread_dstream.foreachRDD(lambda rdd: rdd.foreachPartition(set_redis_avg_spread))

if __name__ == '__main__':
    # Kraken asset pairs for BTC, ETH, and LTC to USD prices
    asset_pairs = ['XXBTZUSD', 'XETHZUSD', 'EOSUSD', 'XLTCZUSD', 'BCHXBT']
    intervals = [1, 5, 15, 30, 60, 240, 1440, 10080, 21600]
    spread_topics = []
    ohlc_topics = []

    for asset_pair in asset_pairs:
        # Spread
        topic_name = '{}_{}'.format('Kraken', 'Spread')
        spread_topics.append(topic_name)

        # for interval in intervals:
            # topic_name = '{}_{}_{}'.format('Kraken', 'OHLC', interval)
            # consumer = FinancialMetricStreamConsumer(interval)
            # consumer.consume(ohlc_topics)

    consumer = SparkStreamConsumer()
    consumer.consume_spreads(spread_topics)
    consumer.start_stream()

