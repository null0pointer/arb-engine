from arb_adapter import ArbitrageExchangeAdapter

from time import sleep
import time

import kraken

class KrakenAdapter(ArbitrageExchangeAdapter):
    
    __order_book = []
    
    assets = set()
    pairs = dict()
    
    # highest_bids[<pair>] = (price, size, time)
    highest_bids = dict()
    # lowest_asks[<pair>] = (price, size, time)
    lowest_asks = dict()
            
    def __init__(self):    
        self.kraken_api = kraken.Kraken()
        # self.kraken_api.subscribe_bid_ask_updates('XXBTZUSD', self.bid_ask_update)
        pairs_response = self.kraken_api.request_pairs()
        for pair in pairs_response:
            self.pairs[pair['pair']] = {'quote': pair['quote'], 'base': pair['base']}
            self.assets.add(pair['quote'])
            self.assets.add(pair['base'])
            self.highest_bids[pair['pair']] = (None, None, 0)
            self.lowest_asks[pair['pair']] = (None, None, 0)
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
        price, size, time = self.highest_bids[pair]
        return (price, size)

    def lowest_ask(self, pair):
        price, size, time = self.lowest_asks[pair]
        return (price, size)

    def place_market_bid(self, pair, size):
        pass
        
    def place_market_ask(self, pair, size):
        pass
        
    # exchange callback functions
        
    def trigger_update(self):
        self.update_callback(self)
    
    def bid_ask_update(self, pair, bid_price, bid_size, bid_time, ask_price, ask_size, ask_time):
        # print(pair, bid_price, bid_size, bid_time, ask_price, ask_size, ask_time)
        did_update = False
        
        prev_bid_price, prev_bid_size, prev_bid_time = self.highest_bids[pair]
        if int(bid_time) > int(prev_bid_time):
            new_bid_time = bid_time
            new_bid_price = bid_price
            new_bid_size = bid_size
            self.highest_bids[pair] = (new_bid_price, new_bid_size, new_bid_time)
            
            if prev_bid_price != bid_price or prev_bid_size != bid_size:
                did_update = True
                
        prev_ask_price, prev_ask_size, prev_ask_time = self.lowest_asks[pair]
        if int(ask_time) > int(prev_ask_time):
            new_ask_time = ask_time
            new_ask_price = ask_price
            new_ask_size = ask_size
            self.lowest_asks[pair] = (new_ask_price, new_ask_size, new_ask_time)
            
            if prev_ask_price != ask_price or prev_ask_size != ask_size:
                did_update = True
                
        if did_update:
            self.trigger_update()
    