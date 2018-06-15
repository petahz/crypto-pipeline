import time
from producers.kraken_producer import Producer


if __name__ == '__main__':
    # Kraken asset pairs for BTC, ETH, and LTC to USD prices
    asset_pairs = ['XXBTZUSD', 'XETHZUSD', 'XLTCZUSD']
    methods = ['Spread']
    producers = []

    for asset_pair in asset_pairs:
        for method in methods:
            producers.append(Producer(asset_pair, method))

    while True:
        time.sleep(2)
        for producer in producers:
            producer.produce()
