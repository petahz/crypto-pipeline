from decimal import Decimal
import json
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
import redis


r = redis.StrictRedis(host='redis-group.v7ufhi.ng.0001.use1.cache.amazonaws.com', port=6379, db=0)


def set_redis(partition):
    for msg in partition:
        r.set('b', 'test')


class SparkStreamConsumer:
    spark_context = None

    def __init__(self):
        self.sc = SparkContext(appName=self.spark_context)
        self.ssc = StreamingContext(self.sc, 5)

    def consume(self):
        self.ssc.start()
        self.ssc.awaitTermination()


class AverageSpreadConsumer(SparkStreamConsumer):
    spark_context = 'AverageSpread'

    def __init__(self):
        super().__init__()

    def consume(self, topics):
        self.kvs = KafkaUtils.createDirectStream(self.ssc, topics,
                                                 {'metadata.broker.list': 'localhost:9092'})

        # messages come in [timestamp, bid, ask] format, a spread is calculated by (ask-bid)
        parsed = self.kvs.map(lambda v: json.loads(v[1]))

        def calculate_spread(tx):
            asset_pair = tx[3]
            return (asset_pair, Decimal(tx[2]) - Decimal(tx[1]))

        spread_percentage_dstream = parsed.map(calculate_spread).mapValues(lambda x: (x, 1))

        spread_sum_count_dstream = spread_percentage_dstream.reduceByKey(lambda x, y: (x[0]+y[0], x[1]+y[1]))

        average_spread_dstream = spread_sum_count_dstream.mapValues(lambda x: x[0] / x[1])

        average_spread_dstream.foreachRDD(lambda rdd: rdd.foreachPartition(set_redis))

        # average_spread_dstream.pprint()

        super().consume()


if __name__ == '__main__':
    # Kraken asset pairs for BTC, ETH, and LTC to USD prices
    asset_pairs = ['XXBTZUSD', 'XETHZUSD', 'XLTCZUSD', 'BCHXBT']
    methods = ['Spread']
    topics = []

    for asset_pair in asset_pairs:
        for method in methods:
            topic_name = '{}_{}'.format(asset_pair, method)
            topics.append(topic_name)

    consumer = AverageSpreadConsumer()
    consumer.consume(topics)
