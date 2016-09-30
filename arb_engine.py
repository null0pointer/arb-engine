from time import sleep
import time

from kraken_adapter import KrakenAdapter

PAIR = 'XXBTZUSD'

def exchange_update(exchange_adapter):
    print(str(exchange_adapter.highest_bid(PAIR)) + '  -  ' + str(exchange_adapter.lowest_ask(PAIR)))
    pass

if __name__ == "__main__":
    ka = KrakenAdapter(PAIR)
    ka.receive_updates(exchange_update)
    
    while True:
        sleep(1)
