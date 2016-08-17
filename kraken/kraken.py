import krakenex
import _thread
from time import sleep
            
def repeating_public_request(method, params, response_handler, error_handler, interval=0):
    kraken = krakenex.API()
    kraken.set_connection(krakenex.Connection())
    
    while True:
        response = kraken.query_public(method, params)
        errors = response['error']
        if len(errors) > 0:
            error_handler(errors)
        else:
            response_handler(response['result'])
        sleep(interval)

class Kraken:
    
    krakenex = None
    
    def __init__(self):
        _thread.start_new_thread(repeating_public_request, ('Depth', {'pair': 'XETHXXBT', 'count': '1'}, self.depth_response_handler, self.generic_error_handler))
        _thread.start_new_thread(repeating_public_request, ("Depth", {'pair': 'XXBTZUSDasd', 'count': '1'}, self.ticker_response_handler, self.generic_error_handler))
        # _thread.start_new_thread(repeating_public_request, ('Ticker', {'pair': 'XETHXXBT'}, self.ticker_request_callback))

    def depth_response_handler(self, response):
        for key in response:
            pair = response[key]
            highest_bid = pair['bids'][0][0]
            lowest_ask = pair['asks'][0][0]
            print(str(key) + ': bid = ' + str(highest_bid) + " ask = " + str(lowest_ask))
        
    def ticker_response_handler(self, response):
        print('Depth: ' + str(response))
        
    def generic_error_handler(self, errors):
        print('Error: ' + str(errors))