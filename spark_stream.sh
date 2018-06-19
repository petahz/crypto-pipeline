#!/usr/bin/env bash
#

${SPARK_HOME}/bin/spark-submit --packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.3.1 --py-files spark/spark_stream_consumer.py spark/main.py
