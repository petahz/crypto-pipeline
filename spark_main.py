from spark.spark_stream_consumer import AverageSpreadStreamConsumer, FinancialMetricStreamConsumer


if __name__ == '__main__':
    # Kraken asset pairs for BTC, ETH, and LTC to USD prices
    asset_pairs = ['XXBTZUSD', 'XETHZUSD', 'XLTCZUSD', 'BCHXBT']
    intervals = [1, 5, 15, 30, 60, 240, 1440, 10080, 21600]
    spread_topics = []
    ohlc_topics = []

    for asset_pair in asset_pairs:
        # Spread
        topic_name = '{}_{}'.format(asset_pair, 'Spread')
        spread_topics.append(topic_name)

        for interval in intervals:
            topic_name = '{}_{}_{}'.format(asset_pair, 'OHLC', interval)
            ohlc_topics.append(topic_name)

    consumer = AverageSpreadStreamConsumer()
    consumer.consume(spread_topics)

    # consumer = FinancialMetricStreamConsumer()
    # consumer.consume(ohlc_topics)