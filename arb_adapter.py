from abc import ABCMeta, abstractmethod

class ArbitrageExchangeAdapter(metaclass=ABCMeta):
    
    @abstractmethod
    def receive_updates(self, callback):
        pass
        
    @abstractmethod
    def available_pairs(self):
        pass
    
    # returns (<price>, <size>)
    @abstractmethod
    def highest_bid(self, pair):
        pass
        
    # returns (<price>, <size>)
    @abstractmethod
    def lowest_ask(self, pair):
        pass
        
    @abstractmethod
    def place_market_bid(self, pair, size):
        pass
        
    @abstractmethod
    def place_market_ask(self, pair, size):
        pass
