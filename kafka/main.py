from producers.kraken_producer import Producer
import time


if __name__ == '__main__':
    # Kraken asset pairs for BTC, ETH, and LTC to USD prices
    asset_pairs = ['XXBTZUSD', 'XETHZUSD', 'XLTCZUSD', 'BCHXBT', 'XETHXXBT', 'XLTCXXBT']
    methods = ['Spread']
    batch_methods = ['Depth']
    producers = []

    for asset_pair in asset_pairs:
        for method in methods:
            producers.append(Producer(asset_pair, method))

    while True:
        time.sleep(2)
        for producer in producers:
            producer.produce()
