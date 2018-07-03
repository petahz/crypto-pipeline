import asyncio
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
        asset_pairs = ['XXBTZUSD', 'XETHZUSD', 'EOSUSD', 'XLTCZUSD', 'BCHUSD']
        # asset_pairs = [asset_pair for asset_pair in response['result'].keys() if 'USD' in asset_pair]
        methods = ['Spread']
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
            futures = [producer.produce_confluent() for producer in producers]
            loop = asyncio.get_event_loop()
            loop.run_until_complete(asyncio.wait(futures))
            # for producer in producers:
            #     producer.produce_confluent()
