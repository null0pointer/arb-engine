from autobahn.asyncio.wamp import ApplicationSession
from autobahn.asyncio.wamp import ApplicationRunner

poloniex_instance = None

class Poloniex:
    
    def __init__(self):
        self.runner = ApplicationRunner("wss://api.poloniex.com:443", "realm1", extra={'poloniex': self})
        
    def start(self):
        poloniex_instance = self
        print(poloniex_instance)
        self.runner.run(PoloniexComponent)
        
    def onTicker(self, currencyPair, last, lowestAsk, highestBid, percentChange, baseVolume, quoteVolume, isFrozen, high, low):
        print(currencyPair, last)

class PoloniexComponent(ApplicationSession):
    def onConnect(self):
        self.poloniex = self.config.extra['poloniex']
        self.join(self.config.realm)

    def onJoin(self, details):
        try:
            yield from self.subscribe(self.poloniex.onTicker, 'ticker')
        except Exception as e:
            print("Could not subscribe to topic:", e)


def main():
    polo = Poloniex()
    polo.start()

if __name__ == "__main__":
    main()