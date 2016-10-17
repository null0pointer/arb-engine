from autobahn.asyncio.wamp import ApplicationSession
from autobahn.asyncio.wamp import ApplicationRunner
from asyncio import coroutine
from time import sleep
import threading

def start_poloniex_runner(delegate):
    runner = ApplicationRunner("wss://api.poloniex.com:443", "realm1", extra={'poloniex': delegate})
    runner.run(PoloniexComponent)

class Poloniex:
    
    def __init__(self):
        self.bids = []
        self.asks = []
        
    def start(self):
        thr = threading.Thread(target=start_poloniex_runner, args=(self,), kwargs={})
        thr.start()
        # _thread.start_new_thread(self.runner.run, (PoloniexComponent,))
        # self.runner.run(PoloniexComponent)
        
    def onTicker(self, currencyPair, last, lowestAsk, highestBid, percentChange, baseVolume, quoteVolume, isFrozen, high, low):
        # print(currencyPair, last)
        pass
        
    def onMarketUpdate(self, *args, seq=0):
        for update in args:
            update_type = update['type']
            if update_type == 'orderBookModify':
                self.onOrderbookUpdate(update['data'], seq)
            elif update_type == 'orderBookRemove':
                self.onOrderbookRemove(update['data'], seq)
            elif update_type == 'newTrade':
                self.onTrade(update['data'], seq)
            
    def onOrderbookUpdate(self, data, time):
        if data['type'] == 'bid':
            self.updateBid(float(data['rate']), float(data['amount']), int(time))
        elif data['type'] == 'ask':
            self.updateAsk(float(data['rate']), float(data['amount']), int(time))
    
    def onOrderbookRemove(self, data, time):
        if data['type'] == 'bid':
            self.updateBid(float(data['rate']), 0, int(time))
        elif data['type'] == 'ask':
            self.updateAsk(float(data['rate']), 0, int(time))
        
    def onTrade(self, data, time):
        # print('TRADE', data)
        pass
    
    def updateBid(self, price, amount, time):
        index = 0
        while index < len(self.bids):
            if price > self.bids[index].price:
                break
            index += 1
            
        if index < len(self.bids):
            if amount > 0:
                if price == self.bids[index].price:
                    if time > self.bids[index].time:
                        self.bids[index].amount = amount
                        self.bids[index].time = time
                else:
                    self.bids.insert(index, Order(price, amount, time))
            else:
                if price == self.bids[index].price:
                    self.bids.pop(index)
        else:
            self.bids.append(Order(price, amount, time))
            
        print('BIDS: ' + str(self.bids))
        
    def updateAsk(self, price, amount, time):
        index = 0
        while index < len(self.asks):
            if price < self.asks[index].price:
                break
            index += 1
            
        if index < len(self.asks):
            if amount > 0:
                if price == self.asks[index].price:
                    if time > self.asks[index].time:
                        self.asks[index].amount = amount
                        self.asks[index].time = time
                else:
                    self.asks.insert(index, Order(price, amount, time))
            else:
                if price == self.asks[index].price:
                    self.asks.pop(index)
        else:
            self.asks.append(Order(price, amount, time))
            
        print('ASKS: ' + str(self.asks))
        
class Order:
    def __init__(self, price, amount, time):
        self.price = price
        self.amount = amount
        self.time = time
        
    def __repr__(self):
        # return '<' + str(self.price) + ', ' + str(self.amount) + '>'
        return '<' + str(self.price) + '>'

class PoloniexComponent(ApplicationSession):
    
    def onConnect(self):
        self.poloniex = self.config.extra['poloniex']
        self.join(self.config.realm)

    @coroutine
    def onJoin(self, details):
        try:
            yield from self.subscribe(self.poloniex.onTicker, 'ticker')
            yield from self.subscribe(self.poloniex.onMarketUpdate, 'BTC_XMR')
        except Exception as e:
            print("Could not subscribe to topic:", e)


def main():
    polo = Poloniex()
    polo.start()
    
    while True:
        print('lol')
        sleep(1)

if __name__ == "__main__":
    main()