import biki.spot_api as spot

if __name__ == '__main__':

    api_key = 'd7e4d03168ac95fca79ffd60a9dc3632'
    secretkey = '23dd2c1b3090b5fw03a4b5f0af428cb1'

    # spot api test
    spotAPI = spot.SpotAPI(api_key, secretkey)
    result = spotAPI.get_account()
    # result = spotAPI.get_all_order('btcusdt')
    # result = spotAPI.get_all_trade('btcusdt')
    # result = spotAPI.cancel_order(39,'btcusdt')
    # result = spotAPI.cancel_order_all('btcusdt')
    # result = spotAPI.create_order('btcusdt', 'limit', 'buy', 1, 9000)
    # result = spotAPI.create_order('btcusdt', 'market', 'sell', 3.333)
    # result = spotAPI.get_all_ticker()
    # result = spotAPI.get_records('btcusdt', 30)
    # result = spotAPI.get_ticker('btcusdt')
    # result = spotAPI.get_trades('btcusdt')
    # result = spotAPI.get_market()
    # result = spotAPI.get_market_dept('btcusdt', 'step0')
    # result = spotAPI.create_and_cancel_mass_orders('btcusdt', create_orders=[{'side':'buy', 'type':'market', 'volume':1000},{'side':'buy', 'type':'limit', 'volume':1.5, 'price':10000}], cancel_orders=[24,25])
    # result = spotAPI.create_and_cancel_mass_orders('btcusdt', create_orders=[{'side': 'buy', 'type': 'limit', 'volume': 2,'price': 10000},{'side': 'buy', 'type': 'limit', 'volume': 1.5,'price': 10000}])
    # result = spotAPI.create_and_cancel_mass_orders('btcusdt', cancel_orders=[44,45])
    # result = spotAPI.get_new_order('btcusdt')
    # result = spotAPI.get_order_info(30, 'btcusdt')
    # result = spotAPI.get_symbols()

    print(result)
