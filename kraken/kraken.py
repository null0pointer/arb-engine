import krakenex

class Kraken:
    
    krakenex = None
    
    def __init__(self):
        self.krakenex = krakenex.API()
        print(self.krakenex.query_public('Depth', {'pair': 'XXBTZUSD', 'count': '1'}))