import krakenex
import threading

class Kraken:
    
    krakenex = None
    update_interval = 10
    
    def __init__(self):
        self.btckrakenex = krakenex.API()
        self.btckrakenex.set_connection(krakenex.Connection())
        
        self.ethkrakenex = krakenex.API()
        self.ethkrakenex.set_connection(krakenex.Connection())
        
        self.btcthread = threading.Thread(target = self.update_depth(self.btckrakenex, 'XXBTZUSD'))
        self.btcthread.daemon = True
        self.btcthread.start()
        
        print('got here')
        
        self.eththread = threading.Thread(target = self.update_depth(self.ethkrakenex, 'XETHXXBT'))
        self.eththread.daemon = True
        self.eththread.start()
        
    def request_depth(self, api, pair):
        return api.query_public('Depth', {'pair': pair, 'count': '1'})
        
    def update_depth(self, api, pair):
        while True:
            print(self.request_depth(api, pair))