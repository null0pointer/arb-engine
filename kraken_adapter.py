from arb_adapter import ArbitrageExchangeAdapter

from time import sleep
import time

import kraken

class KrakenAdapter(ArbitrageExchangeAdapter):
    
    __order_book = []
    
    assets = set()
    pairs = dict()
    
    # highest_bids[<pair>] = (price, size)
    highest_bids = dict()
    # lowest_asks[<pair>] = (price, size)
    lowest_asks = dict()
            
    def __init__(self):    
        self.kraken_api = kraken.Kraken()
        # self.kraken_api.subscribe_bid_ask_updates('XXBTZUSD', self.bid_ask_update)
        pairs_response = self.kraken_api.request_pairs()
        for pair in pairs_response:
            self.pairs[pair['pair']] = {'quote': pair['quote'], 'base': pair['base']}
            self.assets.add(pair['quote'])
            self.assets.add(pair['base'])
            print(str(pair['pair']) + ' = ' + str(pair['quote']) + ' / ' + str(pair['base']))
            
        print('assets = ' + str(self.assets))
        
        for pair in self.pairs:
            if (pair[-2:] != '.d'):
                self.kraken_api.subscribe_bid_ask_updates(pair, self.bid_ask_update)

    # ArbitrageExchangeAdapter functions

    def receive_updates(self, update_callback):
        self.update_callback = update_callback
        
    def available_pairs(self):
        return self.pairs

    def highest_bid(self, pair):
        return self.__highest_bid

    def lowest_ask(self, pair):
        return self.__lowest_ask

    def place_market_bid(self, pair, size):
        pass
        
    def place_market_ask(self, pair, size):
        pass
        
    # exchange callback functions
        
    def trigger_update(self):
        self.update_callback(self)
    
    def bid_ask_update(self, pair, bid_price, bid_size, bid_time, ask_price, ask_size, ask_time):
        print(pair, bid_price, bid_size, bid_time, ask_price, ask_size, ask_time)
    