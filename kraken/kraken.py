import krakenex
import threading

class Kraken:
    
    krakenex = None
    update_interval = 10
    
    def __init__(self):
        self.krakenex = krakenex.API()
        self.krakenex.set_connection(krakenex.Connection())
        self.thread = threading.Thread(target = self.update_depth())
        self.thread.daemon = True
        self.thread.start()
        
    def request_depth(self, pair):
        return self.krakenex.query_public('Depth', {'pair': pair, 'count': '1'})
        
    def update_depth(self):
        while True:
            print(self.request_depth('XXBTZUSD'))