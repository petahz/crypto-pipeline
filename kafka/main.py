from krakenex import API
import time

from kafka.producers.kraken_producer import KrakenProducer


def start_kraken_producer():
    response = API().query_public('AssetPairs', {})

    if len(response['error']) > 0:
        for e in response['error']:
            print('Error: ', e)
    else:
        # Kraken asset pairs for BTC, ETH, and LTC to USD prices
        asset_pairs = response['result'].keys()
        methods = ['Spread', 'Depth', 'OHLC', 'Trades']
        intervals = [1, 5, 15, 30, 60, 240, 1440, 10080, 21600]
        producers = []

        for asset_pair in asset_pairs:
            for method in methods:
                if method == 'OHLC':
                    for interval in intervals:
                        producers.append(KrakenProducer(asset_pair, method, interval))
                else:
                    producers.append(KrakenProducer(asset_pair, method))

        while True:
            time.sleep(2)
            for producer in producers:
                producer.produce_confluent()
