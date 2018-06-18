from datetime import timedelta
from decimal import Decimal
import json
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
import redis
import time

KAFKA_NODES = ['ec2-52-44-121-53.compute-1.amazonaws.com:9092', 'ec2-52-22-234-28.compute-1.amazonaws.com:9092',
                 'ec2-52-45-23-147.compute-1.amazonaws.com:9092', 'ec2-18-207-65-150.compute-1.amazonaws.com:9092']

r = redis.StrictRedis(host='redis-ec-cluster.v7ufhi.clustercfg.use1.cache.amazonaws.com', port=6379,
                              db=0)

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

        def set_redis(partition):
            for msg in partition:
                # r.set('a', 'test')
                pass

        average_spread_dstream.foreachRDD(lambda rdd: rdd.foreachPartition(set_redis))

        # average_spread_dstream.pprint()

        super().consume()
