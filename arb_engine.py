from time import sleep
import time

import bitfinex
from bitfinex_adapter import BitfinexAdapter

def exchange_update(exchange_adapter):
    print(exchange_adapter.last_price())

if __name__ == "__main__":
    ba = BitfinexAdapter()
    ba.receive_updates(exchange_update)
    
    while True:
        sleep(1)
