from chalice import Chalice
from itertools import chain, starmap
import requests
import yfinance as yf

app = Chalice(app_name='assetprice')

@app.route('/stock')
def stock_price():
    symbols = app.current_request.query_params.get('symbols').split(',')
    out = {}
    for symbol in symbols:
        try:
            ticker = yf.Ticker(symbol)
            todays_data = ticker.history(period='1d')
            out[symbol] = todays_data['Close'][0]
        except:
            continue
    return out
    
@app.route('/crypto')
def crypto_price():
    symbols = app.current_request.query_params.get('symbols')
    r = requests.get('https://min-api.cryptocompare.com/data/pricemulti?fsyms={}&tsyms=USD'.format(symbols))
    return flatten_json(r.json())

def flatten_json(dictionary):
    """Flatten a nested json file"""

    def unpack(parent_key, parent_value):
        """Unpack one level of nesting in json file"""
        # Unpack one level only!!!
        
        if isinstance(parent_value, dict):
            for key, value in parent_value.items():
                temp1 = parent_key + '_' + key
                yield temp1, value
        elif isinstance(parent_value, list):
            i = 0 
            for value in parent_value:
                temp2 = parent_key + '_'+str(i) 
                i += 1
                yield temp2, value
        else:
            yield parent_key, parent_value    

            
    # Keep iterating until the termination condition is satisfied
    while True:
        # Keep unpacking the json file until all values are atomic elements (not dictionary or list)
        dictionary = dict(chain.from_iterable(starmap(unpack, dictionary.items())))
        # Terminate condition: not any value in the json file is dictionary or list
        if not any(isinstance(value, dict) for value in dictionary.values()) and \
           not any(isinstance(value, list) for value in dictionary.values()):
            break

    return dictionary