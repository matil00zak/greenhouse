import Adafruit_DHT
import time
import board
import RPi.GPIO as GPIO
import adafruit_tsl2591
import busio
import sensors
from threading import Lock

class Device:
    def __init__(self, id, type_, pin, default_state="LOW"):
        self.id = id
        self.type = type_
        self.pin = pin
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        self.initial = GPIO.HIGH if default_state == "HIGH" else GPIO.LOW
        GPIO.setup(self.pin, GPIO.OUT, initial = self.initial)

    def turn_on(self):
        raise NotImplementedError("Subklasa musi zaimplementować turn_on()")

    def turn_off(self):
        raise NotImplementedError("Subklasa musi zaimplementować turn_off()")

    def impulse(self, impulse_length):
        with Lock():
            GPIO.output(self.pin, GPIO.HIGH)
            time.sleep(impulse_length)
            GPIO.output(self.pin, GPIO.LOW)

class Humidifier(Device):
    def __init__(self, id, pin):
            super().__init__(id=id, type_="Humidifier", pin = pin)

    def turn_on(self):
        print(f"{self.id}: Wysyłam impuls 0.2 do uruchomienia")
        self.impulse(0.2)

    def turn_off(self):
        print(f"{self.id}: Wysyłam impuls 4 s do wyłączenia")
        self.impulse(4)

    def work_for(self, duration):
        print(f"{self.id}: uruchamiam na {duration} sekundy")        
        self.turn_on()
        time.sleep(duration)
        self.turn_off()

class Fan_normal(Device):
    def __init__(self, id, pin):
            super().__init__(id=id, type_="Vent", pin = pin, default_state = "HIGH")

    def turn_on(self):
        print(f"{self.id}: generuje stan pracy")
        GPIO.output(self.pin, GPIO.LOW)
        

    def turn_off(self):
        print(f"{self.id}: generuje stan spoczynku")
        GPIO.output(self.pin, GPIO.HIGH)

    def work_for(self, duration):
        print(f"{self.id}: uruchamiam na {duration} sekundy")
        self.turn_on()
        time.sleep(duration)
        self.turn_off()

class Fan_special(Device):
    def __init__(self, id, pin):
            super().__init__(id=id, type_="Mover", pin = pin)

    def turn_on(self):
        print(f"{self.id}: Wysyłam impuls do uruchomienia")
        self.impulse(0.2)

    def turn_off(self):
        print(f"{self.id}: Wysyłam impuls do wyłączenia") 
        for i in range(3):
            self.impulse(0.2)
            time.sleep(0.3)

    def work_for(self, duration):
        print(f"{self.id}: uruchamiam na {duration} sekundy")
        self.turn_on()
        time.sleep(duration)
        self.turn_off()










