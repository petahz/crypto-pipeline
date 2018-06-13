from .coinapi_v1 import CoinAPIv1
from urllib.error import HTTPError

import boto3
import datetime
import json
import os


def get():
    # Create an S3 client
    s3 = boto3.client('s3')

    api_key = os.environ['COIN_API_KEY']
    bucket_name = 'crypto-pipeline'

    if api_key is None:
        print('COIN_API_KEY needs to be set as an environment variable.')

    coin_api = CoinAPIv1(api_key)

    # Get historical orderbook data for interested crypto assets
    assets = [{'exchange_id': 'COINBASE', 'coin_id': 'BTC'}]

    for asset in assets:
        data = []
        year = 2017
        month = 1
        day = 2
        start_date = datetime.date(year, month, day)
        exchange_id = asset['exchange_id']
        coin_id = asset['coin_id']

        symbol_id = '{0}_SPOT_{1}_USD'.format(exchange_id, coin_id)

        try:
            data = coin_api.orderbooks_historical_data(symbol_id,
                {'time_start': start_date.isoformat(), 'limit': 9000, 'limit_levels': 5})
            print('length: ', len(data))
        except HTTPError as e:
            print('Error: ', HTTPError)

        if len(data) > 0:
            key = '{0}/{1}/{2}/{3}/{4}'.format(coin_id, exchange_id, year, month.strftime('%B'), day)
            s3.put_object(Body=json.dumps(data), Bucket=bucket_name, Key=key)
        else:
            break
