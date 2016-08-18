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
    pairs = []
    bid_ask_callbacks = dict()
    
    def __init__(self):
        # _thread.start_new_thread(repeating_public_request, ('Depth', {'pair': 'XXBTZUSD', 'count': '1'}, self.depth_response_handler, self.generic_error_handler))
        # _thread.start_new_thread(repeating_public_request, ("Ticker", {'pair': 'XXBTZUSD'}, self.ticker_response_handler, self.generic_error_handler))
        pass
        
    def subscribe_bid_ask_updates(self, pair, callback):
        self.bid_ask_callbacks[pair] = callback
        _thread.start_new_thread(repeating_public_request, ('Depth', {'pair': pair, 'count': '1'}, self.depth_subscription_response_handler, self.generic_error_handler))

    def depth_subscription_response_handler(self, response):
        for pair in response:
            depth = response[pair]
            bid_price = depth['bids'][0][0]
            bid_size = depth['bids'][0][1]
            bid_time  = depth['bids'][0][2]
            ask_price = depth['asks'][0][0]
            ask_size = depth['asks'][0][1]
            ask_time  = depth['asks'][0][2]
            self.invoke_bid_ask_callback(pair, bid_price, bid_size, bid_time, ask_price, ask_size, ask_time)
        
    def ticker_response_handler(self, response):
        print('Ticker: ' + str(response))
        
    def generic_error_handler(self, errors):
        print('Error: ' + str(errors))
        
    def invoke_bid_ask_callback(self, pair, bid_price, bid_size, bid_time, ask_price, ask_size, ask_time):
        if pair in self.bid_ask_callbacks:
            callback = self.bid_ask_callbacks[pair]
            callback(pair, bid_price, bid_size, bid_time, ask_price, ask_size, ask_time)