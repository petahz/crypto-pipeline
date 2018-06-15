from producers.kraken_producer import Producer


if __name__ == '__main__':
    # Kraken asset pairs for BTC, ETH, and LTC to USD prices
    asset_pairs = ['XXBTZUSD', 'XETHZUSD', 'XLTCZUSD']
    methods = ['Spread']

    for asset_pair in asset_pairs:
        for method in methods:
            producer = Producer(asset_pair, method)
            topic_name = producer.produce()

            consumer = AverageSpreadConsumer(topic_name)
            consumer.consume()
