from dataclasses import dataclass

import adafruit_dht
import board


@dataclass
class Dht11:
    dhtDevice = adafruit_dht.DHT11(board.D4)
