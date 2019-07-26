import websocket
from websocket import create_connection
from websocket._exceptions import WebSocketConnectionClosedException
import gzip
import time
import json
from biki.consts import *

try:
    import thread
except ImportError:
    import _thread as thread


def on_error(ws, error):
    print('### error ###')
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    print('### opened ###')

    # sub trade ticker
    ws.send('{"event": "sub", "params": {"channel": "market_btcusdt_trade_ticker", "cb_id": "custom string"}}')
    time.sleep(1)

    # sub kline
    ws.send('{"event":"sub","params":{"channel":"market_btcusdt_kline_1min","cb_id":"custom string"}}')
    time.sleep(1)

    # sub depth
    ws.send('{"event":"sub","params":{"channel":"market_btcusdt_depth_step0","cb_id":"custom string","asks":150,"bids":150}}')

def on_message(ws, message):
    result = gzip.decompress(message).decode('utf-8')
    if result[:7] == '{"ping"':
        ts = result[8:21]
        pong = '{"pong":' + ts + '}'
        ws.send(pong)
    else:
        print(result)


if __name__ == '__main__':
    # Debug
    # websocket.enableTrace(True)
    ws = websocket.WebSocketApp(WS_URL,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close,
                                on_open=on_open)
    ws.run_forever()

