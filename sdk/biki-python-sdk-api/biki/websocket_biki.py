from consts import *
from retry.api import retry_call
from websocket import create_connection,WebSocketException
import json
import gzip
import ssl
import requests
import socket

last_ts = 0
symbol = 'btcusdt'

def run_forever():

    ws = None

    while 1:
        try:
            if ws is None:
                raise ValueError

            frame = ws.recv()
            frame = gzip.decompress(frame).decode('utf-8')
            frame = json.loads(frame, parse_float=str)

        except (WebSocketException, ssl.SSLError, socket.error, IOError, ValueError,) as e:

            ws = retry_call(create_ws,
                            exceptions=(requests.RequestException, WebSocketException, ssl.SSLError, socket.error,),
                            delay=0.1,
                            max_delay=30,
                            backoff=1.1
                            )
            continue

        on_message(ws, frame)


def create_ws():
    _ws = create_connection(WS_URL)
    _ws.send("""{"event": "sub", "params": {"channel": "market_%s_depth_step0", "cb_id": "id1"}}""" % symbol)
    return _ws


def on_message(ws, msg):
    global last_ts
    if 'ping' in msg:
        ws.send('{"pong":%s}' % msg['ping'])
        return

    if 'channel' not in msg:
        return

    if msg['ts'] < last_ts:
        return

    print(msg)

    last_ts = msg['ts']

if __name__ == '__main__':
    run_forever()