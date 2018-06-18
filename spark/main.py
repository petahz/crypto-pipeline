from spark_stream_consumer import AverageSpreadConsumer


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
