#!/bin/bash

${SPARK_HOME}/bin/spark-submit --deploy-mode cluster --packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.3.1 --py-files spark/spark_stream_consumer.py spark_main.py
