import boto3
import datetime
import os

from libraries.coinapi_v1 import CoinAPIv1


# Create an S3 client
s3 = boto3.client('s3')

api_key = os.environ['COIN_API_KEY']
bucket_name = 'crypto-pipeline'

if api_key is None:
    print('COIN_API_KEY needs to be set as an environment variable.')

api = CoinAPIv1(api_key)

# Get historical orderbook data for interested crypto assets
start_of_2017 = datetime.date(2017, 1, 1).isoformat()
coinbase_ids = ['BTC']

for coin_id in coinbase_ids:
    symbol_id = 'COINBASE_SPOT_{}_USD'.format(coin_id)
    data = api.orderbooks_historical_data(symbol_id, {'time_start': start_of_2017})

    s3.upload_fileobj(data, bucket_name, coin_id)

