from dataclasses import dataclass

import adafruit_dht
import board
import busio
import adafruit_ccs811


@dataclass
class Dht11:
    dhtDevice = adafruit_dht.DHT11(board.D4)


@dataclass
class Dht22:
    dhtDevice = adafruit_dht.DHT22(board.D22, use_pulseio=False)


@dataclass
class Ccs811:
    i2c_bus = busio.I2C(board.SCL, board.SDA)
    ccs811 = adafruit_ccs811.CCS811(i2c_bus)
