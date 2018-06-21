from kafka.producers.kraken_producer import KrakenProducer
import time


def start_kraken_producer():
    # Kraken asset pairs for BTC, ETH, and LTC to USD prices
    asset_pairs = ['XXBTZUSD', 'XETHZUSD', 'XLTCZUSD', 'BCHXBT', 'XETHXXBT', 'XLTCXXBT']
    methods = ['Spread']
    batch_methods = ['Depth']
    producers = []

    for asset_pair in asset_pairs:
        for method in methods:
            producers.append(KrakenProducer(asset_pair, method))

    while True:
        time.sleep(2)
        for producer in producers:
            producer.produce_confluent()
