import krakenex
import threading
import _thread
from time import sleep

# class RepeatingRequestThread(threading.Thread):
#
#     def __init__(self, command, params, callback, interval=0, private=False, api_key='', api_secret=''):
#         self.command = command
#         self.params = params
#         self.callback = callback
#         self.interval = interval
#         self.private = private
#
#         self.krakenex = krakenex.API(key=api_key, secret=api_secret)
#         self.krakenex.set_connection(krakenex.Connection())
#
#         threading.Thread.__init__(self)
#         self.daemon = True
#
#     def run(self):
#         while True:
#             response = None
#             if self.private:
#                 response = self.krakenex.query_private(self.command, self.params)
#             else:
#                 response = self.krakenex.query_public(self.command, self.params)
#             self.callback(response)
#
#             sleep(self.interval)
            
def repeating_public_request(method, params, callback, interval=0):
    kraken = krakenex.API()
    kraken.set_connection(krakenex.Connection())
    
    while True:
        response = kraken.query_public(method, params)
        callback(response)
        sleep(interval)

class Kraken:
    
    krakenex = None
    
    def __init__(self):
        _thread.start_new_thread(repeating_public_request, ("Depth", {'pair': 'XETHXXBT', 'count': '1'}, self.request_callback))
        _thread.start_new_thread(repeating_public_request, ("Depth", {'pair': 'XXBTZUSD', 'count': '1'}, self.request_callback))
        # self.start_updating_depth()
        # print('got here')
        # self.start_updating_ticker()
        
    def request_callback(self, response):
        print(response)
        
    def start_updating_depth(self):
        request = RepeatingRequestThread('Depth', {'pair': 'XETHXXBT', 'count': '1'}, self.request_callback)
        request.run()
        
    def start_updating_ticker(self):
        request = RepeatingRequestThread('Ticker', {'pair': ['XETHXXBT']}, self.request_callback)
        request.run()
        
    def request_depth(self, api, pair):
        return api.query_public('Depth', {'pair': pair, 'count': '1'})
        
    def request_ticker(self, api, pairs):
        pairs_string = ','.join(pairs)
        return api.query_public('Ticker', {'pair': pairs_string})
        
    def received_depth_update(self, pair, response):
        result = response['result'][pair]
        highest_bid = result['bids'][0][0]
        lowest_ask = result['asks'][0][0]
        print(str(pair) + ': bid = ' + str(highest_bid) + " ask = " + str(lowest_ask))
        
    def received_ticker_update(self, pairs, response):
        result = response['result']
        for pair in pairs:
            pair_ticker = result[pair]
            asks = pair_ticker['a']
            bids = pair_ticker['b']
            print(str(pair) + ': bids = ' + str(bids) + ' asks = ' + str(asks))
        
    def update_depth(self, api, pair):
        while True:
            response = self.request_depth(api, pair)
            self.received_depth_update(pair, response)
            
    def update_ticker(self, api, pairs):
        while True:
            response = self.request_ticker(api, pairs)
            self.received_ticker_update(pairs, response)