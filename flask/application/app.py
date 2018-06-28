from flask import request, render_template, jsonify, url_for, redirect, g
from flask_socketio import SocketIO, emit
from .models import User
from index import app, db
import redis
from sqlalchemy.exc import IntegrityError
import time
from .utils.auth import generate_token, requires_auth, verify_token

r = redis.StrictRedis(host='redis-group.v7ufhi.ng.0001.use1.cache.amazonaws.com', port=6379, db=0)

socketio = SocketIO(app)
def emit_data_from_redis():
    data = {}
    for key in r.scan_iter():
        if r.type(key) == b'hash':
            data[key.decode()] = {
                'bid': r.hget(key, 'bid').decode(),
                'ask': r.hget(key, 'ask').decode(),
                'spread': r.hget(key, 'spread').decode() if r.hget(key, 'spread') is not None else None,
                'avg_spread': r.hget(key, 'avg_spread').decode(),
            }
    print('data: ', data)
    emit('liveData', data)

# Handle the webapp connecting to the websocket
@socketio.on('connect')
def test_connect():
    print('someone connected to websocket')
    emit_data_from_redis()

@socketio.on('next')
def next_data(success):
    print('next_data')
    time.sleep(1)
    emit_data_from_redis()

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/<path:path>', methods=['GET'])
def any_root_path(path):
    return render_template('index.html')
