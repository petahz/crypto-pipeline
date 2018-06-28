#!/bin/bash

${SPARK_HOME}/bin/spark-submit --master spark://ec2-34-235-103-8.compute-1.amazonaws.com:7077 --packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.3.1 --py-files spark/spark_stream_consumer.py spark_main.py
