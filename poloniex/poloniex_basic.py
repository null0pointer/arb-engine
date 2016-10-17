from poloniex_api_wrapper import PoloniexAPIWrapper

class Poloniex:
    
    def __init__(self):
        self.poloniex = PoloniexAPIWrapper('', '')
        print(self.poloniex.returnOrderBook('BTC_XMR'))
        
polo = Poloniex()