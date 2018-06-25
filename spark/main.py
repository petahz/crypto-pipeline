from spark_stream_consumer import AverageSpreadConsumer, FinancialMetricConsumer


if __name__ == '__main__':
    # Kraken asset pairs for BTC, ETH, and LTC to USD prices
    asset_pairs = ['XXBTZUSD', 'XETHZUSD', 'XLTCZUSD', 'BCHXBT']
    spread_topics = []
    ohlc_topics = []

    for asset_pair in asset_pairs:
        # Spread
        topic_name = '{}_{}'.format(asset_pair, 'Spread')
        spread_topics.append(topic_name)

    consumer = AverageSpreadConsumer()
    consumer.consume(spread_topics)

    consumer = FinancialMetricConsumer()
    consumer.consume(ohlc_topics)
