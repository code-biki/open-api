import hmac
import base64
import time
import hashlib
import collections
from . import consts as c

def keysort(dictionary):
    return collections.OrderedDict(sorted(dictionary.items(), key=lambda t: t[0]))

def sign(params, api_secret):
    message = ''
    query = keysort(params)
    keys = list(query.keys())
    for i in range(0, len(keys)):
        key = keys[i]
        message += key
        message += str(query[key])
    md = hashlib.md5()
    # print('sign message:', message)
    md.update((message + api_secret).encode(encoding='utf-8'))
    msg_md5 = md.hexdigest()
    return msg_md5

def parse_params_to_str(params):
    url = '?'
    for key, value in params.items():
        url = url + str(key) + '=' + str(value) + '&'

    return url[0:-1]

def get_header():
    header = dict()
    header[c.CONTENT_TYPE] = c.APPLICATION_FORM

    return header

def get_timestamp():
    timestamp = int(time.time())
    return timestamp


def signature(timestamp, method, request_path, body, secret_key):
    if str(body) == '{}' or str(body) == 'None':
        body = ''
    message = str(timestamp) + str.upper(method) + request_path + str(body)
    mac = hmac.new(bytes(secret_key, encoding='utf8'), bytes(message, encoding='utf-8'), digestmod='sha256')
    d = mac.digest()
    return base64.b64encode(d)
