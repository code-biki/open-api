import biki.rest_api as restapi

if __name__ == '__main__':

    api_key = 'd7e4d03168ac95fca79ffd60a9dc3632'
    secretkey = '23dd2c1b3090b5fw03a4b5f0af428cb1'

    # REST API
    restAPI = restapi.RestAPI(api_key, secretkey)

    # Public
    result = restAPI.get_symbols()
    result = restAPI.get_all_ticker()
    result = restAPI.get_market()
    result = restAPI.get_ticker('btcusdt')
    result = restAPI.get_trades('btcusdt')
    result = restAPI.get_records('btcusdt', 30)
    result = restAPI.get_market_dept('btcusdt', 'step0')

    # Privite
    result = restAPI.get_account()
    # result = restAPI.get_new_order('btcusdt')
    # result = restAPI.get_all_order('btcusdt')
    # result = restAPI.get_all_trade('btcusdt')
    # result = restAPI.get_order_info(30, 'btcusdt')
    # result = restAPI.create_order('btcusdt', 'limit', 'buy', 1, 9000)
    # result = restAPI.create_order('btcusdt', 'market', 'sell', 3.333)
    # result = restAPI.cancel_order(39,'btcusdt')
    # result = restAPI.cancel_order_all('btcusdt')
    # result = restAPI.create_and_cancel_mass_orders('btcusdt', create_orders=[{'side':'buy', 'type':'market', 'volume':1000},{'side':'buy', 'type':'limit', 'volume':1.5, 'price':10000}], cancel_orders=[100001, 100002])
    # result = restAPI.create_and_cancel_mass_orders('btcusdt', create_orders=[{'side': 'buy', 'type': 'limit', 'volume': 2,'price': 10000},{'side': 'buy', 'type': 'limit', 'volume': 1.5,'price': 10000}])
    # result = restAPI.create_and_cancel_mass_orders('btcusdt', cancel_orders=[1000001, 1000002])

    print(result)

