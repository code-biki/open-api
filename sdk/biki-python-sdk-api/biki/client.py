import requests
from . import consts as c, utils
import json


class Client(object):

    def __init__(self, api_key, api_seceret_key):

        self.API_KEY = api_key
        self.API_SECRET_KEY = api_seceret_key


    def _request(self, method, request_path, params, sign_flag=True):
        if sign_flag:
            timestamp = utils.get_timestamp()
            params['api_key'] = self.API_KEY
            params['time'] = str(timestamp)
            sign = utils.sign(params, self.API_SECRET_KEY)
            params['sign'] = sign

        if method == c.GET:
            request_path = request_path + utils.parse_params_to_str(params)
        # url
        url = c.API_URL + request_path
        # sign & header
        body = params if method == c.POST else {}

        header = utils.get_header()

        # send request
        response = None
        # print("url:", url)
        # print("headers:", header)
        # print("body:", body)
        if method == c.GET:
            response = requests.get(url, headers=header)
        elif method == c.POST:
            response = requests.post(url, data=body, headers=header)
        elif method == c.DELETE:
            response = requests.delete(url, headers=header)

        # exception handle
        if not str(response.status_code).startswith('2'):
            raise response.json()
        return response.json()

    def _request_without_params(self, method, request_path):
        return self._request(method, request_path, {})

    def _request_with_params(self, method, request_path, params):
        return self._request(method, request_path, params)

    def _request_no_sign_params(self, method, request_path, params, sign_flag = False):
        return self._request(method, request_path, params, sign_flag)