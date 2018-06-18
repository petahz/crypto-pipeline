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

        # Filter to spreads in the last 5 seconds
        def last_five_seconds(sp):
            five_seconds_ago = time.time() - timedelta(seconds=5).total_seconds()
            return sp[0] > five_seconds_ago

        recent_spreads_dstream = parsed.filter(last_five_seconds)

        # We use a percentage for a fairer comparison of spread than just the difference
        # Spread % = 2 x (Ask – Bid) / (Ask + Bid) x 100 %
        def spread_percentage(tx):
            percentage = 2 * (Decimal(tx[2]) - Decimal(tx[1])) / ((Decimal(tx[2]) + Decimal(tx[1])) * 100)
            return (tx[3], tx[2] - tx[1])

        spread_percentage_dstream = recent_spreads_dstream.map(spread_percentage).mapValues(lambda x: (x, 1))

        spread_sum_count_dstream = spread_percentage_dstream.reduceByKey(lambda x, y: (x[0]+y[0], x[1]+y[1]))

        average_spread_dstream = spread_sum_count_dstream.mapValues(lambda x: x[0] / x[1])

        r = redis.StrictRedis(host='redis-ec-cluster.v7ufhi.clustercfg.use1.cache.amazonaws.com', port=6379, db=0)

        def store_to_redis(rdd):
            print('pickle')
            # def send_message(partition):
            #     print('am i pickling')
            #     partition.foreach(lambda msg: r.set(self.topic_name, msg))
            #
            # rdd.foreachPartition(send_message)

        average_spread_dstream.foreachRDD(store_to_redis)

        average_spread_dstream.pprint()

        super().consume()
