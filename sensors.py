import Adafruit_DHT
import time
import board
import RPi.GPIO as GPIO
import adafruit_tsl2591
import busio
import sensors



class Sensor:
    def __init__(self, id, type_):
        self.id = id
        self.type = type_

    def read_value(self):
        raise NotImplementedError("Subklasa musi zaimplementować read_value()")


class DHT(Sensor):
    def __init__(self, pin, id):
        super().__init__(id=id, type_="DHT")
        self.sensor = Adafruit_DHT.DHT22
        self.pin = pin


    def read_value(self):
        humidity, temperature = Adafruit_DHT.read_retry(self.sensor, self.pin)
        if humidity is not None and temperature is not None:
            return {
                "id" : self.id,
                "type" : self.type,
                "temp": temperature,
                "hum": humidity,
                }
        else:
            return {
                "id" : self.id,
                "type" : self.type,
                "temp": None,
                "hum": None,
                }

class TSL(Sensor):
    def __init__(self, i2c, id):
            super().__init__(id=id, type_="TSL")
            self.i2c = busio.I2C(board.SCL, board.SDA)
            self.light_sensor = adafruit_tsl2591.TSL2591(self.i2c)
    def read_value(self):
            lux = self.light_sensor.lux
            return {
                "id" : self.id,
                "type" : self.type,
                "lux" : lux
                }

