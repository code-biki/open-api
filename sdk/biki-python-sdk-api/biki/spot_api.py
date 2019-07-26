from .client import Client
from .consts import *
import json


class SpotAPI(Client):

    def __init__(self, api_key, api_seceret_key):
        Client.__init__(self, api_key, api_seceret_key)

    # query account balance
    def get_account(self):
        params = {}
        return self._request_with_params(GET, SPOT_ACCOUNT, params)

    # query all order
    def get_all_order(self, symbol, startdate=None, enddate=None, pagesize=None, page=None, sort=None):
        params = {}
        params['symbol'] = symbol
        if startdate:
            params['startDate'] = startdate
        if enddate:
            params['endDate'] = enddate
        if pagesize:
            params['pageSize'] = pagesize
        if page:
            params['page'] = page
        if sort:
            params['sort'] = sort
        return self._request_with_params(GET, SPOT_ALL_ORDER, params)

    #query all trade
    def get_all_trade(self, symbol, startdate=None, enddate=None, pagesize=None, page=None, sort=None):
        params = {}
        params['symbol'] = symbol
        if startdate:
            params['startDate'] = startdate
        if enddate:
            params['endDate'] = enddate
        if pagesize:
            params['pageSize'] = pagesize
        if page:
            params['page'] = page
        if sort:
            params['sort'] = sort
        return self._request_with_params(GET, SPOT_ALL_TRADE, params)

    #cancel order by order_id
    def cancel_order(self, order_id, symbol):
        params = {}
        params['order_id'] = order_id
        params['symbol'] = symbol
        return self._request_with_params(POST, SPOT_CANCEL_ORDER, params)

    #cancel all order by symbol
    def cancel_order_all(self, symbol):
        params = {}
        params['symbol'] = symbol
        return self._request_with_params(POST, SPOT_CANCEL_ORDER_ALL, params)

    #create order
    def create_order(self, symbol, type, side, volume, price = None, fee_is_user_exchange_coin='0'):
        params = {}
        orderType = '1' if (type == 'limit') else '2'
        params['side'] = side.upper()
        params['type'] = orderType
        params['volume'] = volume
        params['symbol'] = symbol
        params['fee_is_user_exchange_coin'] = fee_is_user_exchange_coin
        if price:
            params['price'] = price
        return self._request_with_params(POST, SPOT_CREATE_ORDER, params)

    #qurey all symbol ticker
    def get_all_ticker(self):
        params = {}
        return self._request_no_sign_params(GET, SPOT_ALL_TICKER, params)

    #qurey k-line records
    def get_records(self, symbol, period):
        params = {}
        params['symbol'] = symbol
        params['period'] = period
        return self._request_no_sign_params(GET, SPOT_RECORDS, params)

    #qurey ticker by symbol
    def get_ticker(self, symbol):
        params = {}
        params['symbol'] = symbol
        return self._request_no_sign_params(GET, SPOT_TICKER, params)

    #qurey trades by symbol
    def get_trades(self, symbol):
        params = {}
        params['symbol'] = symbol
        return self._request_no_sign_params(GET, SPOT_TRADES, params)

    #qurey the latest transaction price of each symbol of currencies
    def get_market(self):
        params = {}
        return self._request_no_sign_params(GET, SPOT_MARKET, params)

    #qurey the depth of buying and selling
    def get_market_dept(self, symbol, type):
        params = {}
        params['symbol'] = symbol
        params['type'] = type
        return self._request_with_params(GET, SPOT_DEPTH, params)

    #mass create and cancel order
    # params example:{'btcusdt',
    # cancel_orders=[1,12,31,234],
    # create_orders=[{'side':'buy', 'type':'market', 'volume':1000},{'side':'buy', 'type':'limit', 'volume':1.5, 'price':10000}]}
    def create_and_cancel_mass_orders(self, symbol, create_orders=None, cancel_orders=None):
        params = {}
        if cancel_orders:
            params['mass_cancel'] = json.dumps(cancel_orders)
        if create_orders:
            request_params = []
            for param in create_orders:
                param['side'] = param['side'].upper()
                param['type'] = '1' if (param['type'] == 'limit') else '2'
                request_params.append(param)
            params['mass_place'] = json.dumps(request_params)
        params['symbol'] = symbol
        return self._request_with_params(POST, SPOT_MASS_REPLACE, params)

    #qurey the current order(including uncompleted and ongoing order)
    def get_new_order(self, symbol, pagesize=None, page=None):
        params = {}
        params['symbol'] = symbol
        if pagesize:
            params['pageSize'] = pagesize
        if page:
            params['page'] = page
        return self._request_with_params(GET, SPOT_NEW_ORDER, params)

    #qurey order details by order_id
    def get_order_info(self, id, symbol):
        params = {}
        params['order_id'] = id
        params['symbol'] = symbol
        return self._request_with_params(GET, SPOT_ORDER_INFO, params)

    #qurey all symbols and precision
    def get_symbols(self):
        params = {}
        return self._request_no_sign_params(GET, SPOT_SYMBOLS, params)