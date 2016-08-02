from abc import ABCMeta, abstractmethod

class ArbitrageExchangeAdapter(metaclass=ABCMeta):
    
    @abstractmethod
    def receive_updates(self, callback):
        pass
    
    @abstractmethod
    def last_price(self):
        pass
    
    @abstractmethod
    def highest_bid(self):
        pass
        
    @abstractmethod
    def lowest_ask(self):
        pass
        
    @abstractmethod
    def place_bid(self, price, size):
        pass
        
    @abstractmethod
    def place_ask(self, price, size):
        pass
