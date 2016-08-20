from arb_adapter import ArbitrageExchangeAdapter

from time import sleep
import time

import kraken

class KrakenAdapter(ArbitrageExchangeAdapter):
    
    __last_price = None
    __highest_bid = None
    __lowest_ask = None
    
    __order_book = []
    
    assets = set()
    pairs = dict()
    prices = dict()
            
    def __init__(self):    
        self.kraken_api = kraken.Kraken()
        # self.kraken_api.subscribe_bid_ask_updates('XXBTZUSD', self.bid_ask_update)
        pairs_response = self.kraken_api.request_pairs()
        for pair in pairs_response:
            self.pairs[pair['pair']] = {'quote': pair['quote'], 'base': pair['base']}
            self.assets.add(pair['quote'])
            self.assets.add(pair['base'])
            print(str(pair['pair']) + ' = ' + str(pair['quote']) + ' / ' + str(pair['base']))
            
        self.initialise_prices()
        print('assets = ' + str(self.assets))
        
        for pair in self.pairs:
            if (pair[-2:] != '.d'):
                self.kraken_api.subscribe_bid_ask_updates(pair, self.bid_ask_update)

    # ArbitrageExchangeAdapter functions

    def receive_updates(self, update_callback):
        self.update_callback = update_callback
        
    def last_price(self):
        return self.__last_price

    def highest_bid(self):
        return self.__highest_bid

    def lowest_ask(self):
        return self.__lowest_ask

    def place_bid(self, price, size):
        pass
        
    def place_ask(self, price, size):
        pass
        
    # exchange callback functions
        
    def trigger_update(self):
        self.update_callback(self)
        
    def ticker_update(self, bid, bid_size, ask, ask_size, daily_change, daily_change_percentage, last_price, volume, high, low):
        self.__last_price = last_price
        self.trigger_update()
    
    # def book_update(self, price, count, amount, clear):
    #     if not clear:
    #         pass
    #     else:
    #         self.__order_book = []
    #         self.__highest_bid = None
    #         self.__lowest_ask = None
    #         self.trigger_update()
    
    def bid_ask_update(self, pair, bid_price, bid_size, bid_time, ask_price, ask_size, ask_time):
        # print(str(pair) + ' bid: ' + str(bid_price) + ' (' + str(bid_size) + ') ask: ' + str(ask_price) + ' (' + str(ask_size) + ')')
        quote = self.pairs[pair]['quote']
        base = self.pairs[pair]['base']
        self.prices[quote][base] = str(ask_price)
        self.prices[base][quote] = str(1/float(bid_price))
        self.print_prices()
    
    def print_prices(self):
        sorted_assets = list(self.assets)
        sorted_assets.sort()
        row_string = '\t'
        for asset in sorted_assets:
            row_string = row_string + asset + '\t'
        print(row_string)
        
        for base in sorted_assets:
            row_string = base + '\t'
            for quote in sorted_assets:
                price = str(self.prices[base][quote])
                row_string = row_string + price[:min(7, len(price))] + '\t'
            print(row_string)
            
        print('\n\n')
        
    def initialise_prices(self):
        for base in self.assets:
            if base not in self.prices:
                self.prices[base] = dict()
            for quote in self.assets:
                if quote not in self.prices[base]:
                    self.prices[base][quote] = '-'
            
    # private functions
    
    def __add_to_order_book(order):
        pass
        
    def __remove_from_order_book(order):
        pass
    