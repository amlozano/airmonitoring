from dataclasses import dataclass

import adafruit_dht
import board


@dataclass
class Dht11:
    dhtDevice = adafruit_dht.DHT11(board.D4)


@dataclass
class Dht22:
    dhtDevice = adafruit_dht.DHT22(board.D22, use_pulseio=False)
