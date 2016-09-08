from time import sleep
import time

from kraken_adapter import KrakenAdapter

def exchange_update(exchange_adapter):
    print(str(exchange_adapter.highest_bid('XXBTZUSD')) + '  -  ' + str(exchange_adapter.lowest_ask('XXBTZUSD')))
    pass

if __name__ == "__main__":
    ka = KrakenAdapter()
    ka.receive_updates(exchange_update)
    
    while True:
        sleep(1)
