import krakenex

class Kraken:
    
    krakenex = None
    update_interval = 10
    
    def __init__(self):
        self.krakenex = krakenex.API()
        print(self.request_depth('XXBTZUSD'))
        
    def request_depth(self, pair):
        return self.krakenex.query_public('Depth', {'pair': pair, 'count': '1'})