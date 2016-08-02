from arb_adapter import ArbitrageExchangeAdapter

from time import sleep
import time

import bitfinex

class BitfinexAdapter(ArbitrageExchangeAdapter):
    
    __last_price = None
    __highest_bid = None
    __lowest_ask = None
    
    __order_book = []
            
    def __init__(self):    
        bfx = bitfinex.BitfinexWebsocket(debug=False)
        # bfx.subscribe_ticker(self.ticker_update)
        bfx.subscribe_book(self.book_update)

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
    
    def book_update(self, price, count, amount, clear):
        if not clear:
            pass
        else:
            self.__order_book = []
            self.__highest_bid = None
            self.__lowest_ask = None
            self.trigger_update()
            
    # private functions
    
    def __add_to_order_book(order):
        pass
        
    def __remove_from_order_book(order):
        pass
    