
import argparse
import board, busio
from sensors import DHT, TSL
from devices import Humidifier, Fan_normal, Fan_special

# Inicjalizacja czujników
dht1 = DHT(4, "DHT 1")
dht2 = DHT(5, "DHT 2")
lux1 = TSL(busio.I2C(board.SCL, board.SDA), "LUX 1")

sensors = {
    "dht1": dht1,
    "dht2": dht2,
    "lux1": lux1
}

# Inicjalizacja urządzeń
humidifier = Humidifier("Nawilzacz", pin=21)
fan_normal = Fan_normal("Wentylator", pin=12)
fan_special = Fan_special("Obracacz", pin=16)

devices = {
    "humidifier": humidifier,
    "fan_normal": fan_normal,
    "fan_special": fan_special
}

# Parser CLI
parser = argparse.ArgumentParser()
parser.add_argument("target")  # all_sensors / humidifier / fan_normal / fan_special / dht1 etc.
parser.add_argument("command") # read / turn_on / turn_off / work_for
parser.add_argument("value", nargs="?", default=None)

args = parser.parse_args()

# Obsługa czujników
if args.target == "all_sensors" and args.command == "read":
    for sid, sensor in sensors.items():
        data = sensor.read_value()
        print(f"{sid}: {data}")

elif args.target in sensors and args.command == "read":
    data = sensors[args.target].read_value()
    print(data)

# Obsługa urządzeń
elif args.target in devices:
    device = devices[args.target]
    if args.command == "turn_on":
        device.turn_on()
    elif args.command == "turn_off":
        device.turn_off()
    elif args.command == "work_for" and args.value:
        device.work_for(float(args.value))
    else:
        print("Nieznana komenda dla urządzenia.")
else:
    print("Nieznany cel.")
