from consumers.consumer import Consumer
from producers.kraken_producer import Producer


if __name__ == '__main__':
    asset_pairs = ['XBTUSD', 'ETHUSD', 'LTCUSD']

    for asset_pair in asset_pairs:
        producer = Producer(asset_pair)
        producer.produce('Spread')

        consumer = Consumer(asset_pair)
        consumer.consume('Spread')