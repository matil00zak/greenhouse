import time
import schedule
import threading
import board
import busio
from devices import Humidifier, Fan_normal, Fan_special
from sensors import DHT, TSL
from logger import log_and_display
import RPi.GPIO as GPIO

GPIO.cleanup()

# === Konfiguracja ===
print_mode = True
HUMIDITY_MIN = 70
HUMIDITY_MAX = 80
HUMIDIFIER_TIME = 20   # sekundy
FAN_NORMAL_TIME = 25
FAN_NORMAL_TIME_2 = 90   # sekundy
FAN_SPECIAL_TIME_2 = 90  
FAN_SPECIAL_TIME = 30 # sekundy

# === Globalny LOCK do zarządzania urządzeniami ===
device_lock = threading.Lock()

# === Inicjalizacja urządzeń ===
humidifier = Humidifier("Nawilzacz", pin=21)
fan_normal = Fan_normal("Wentylator", pin=12)
fan_special = Fan_special("Obracacz", pin=16)

# === Inicjalizacja czujników ===
i2c = busio.I2C(board.SCL, board.SDA)
sensors = [
    DHT(4, "DHT 1"),
    DHT(5, "DHT 2"),
    TSL(i2c, "LUX 1")
]

def get_all_data():
    all_data = [sensor.read_value() for sensor in sensors]
    if print_mode == True:
        print(all_data)
    return all_data


def kontrola_wilgotnosci():
    print("SPRAWDZANIE START")
    data = get_all_data()
    wilgotnosci = [d["hum"] for d in data if d["type"] == "DHT" and d["hum"] is not None]
    if print_mode == True:
        print(wilgotnosci)
    if not wilgotnosci:
        print("Brak danych o wilgotności.")
        return

    avg_hum = sum(wilgotnosci) / len(wilgotnosci)
    print(f"[Wilgotność] Średnia: {avg_hum:.1f}%")
    if avg_hum < HUMIDITY_MIN:
        with device_lock:
            humidifier.work_for(HUMIDIFIER_TIME)
            fan_special.work_for(FAN_SPECIAL_TIME)
    elif avg_hum > HUMIDITY_MAX:
        with device_lock:
            fan_normal.work_for(FAN_NORMAL_TIME)
            fan_special.work_for(FAN_SPECIAL_TIME)
        print("SPRAWDZANIE START")

def wentyluj_powietrze():
    print("WENTYLACJA START")
    with device_lock:
        fan_normal.work_for(FAN_NORMAL_TIME_2)
        fan_special.work_for(FAN_SPECIAL_TIME)
    print("WENTYLACJA STOP")


def mieszaj_powietrze():
    print("MIESZANIE START")
    with device_lock:
        fan_special.work_for(FAN_SPECIAL_TIME_2)
    print("MIESZAINE STOP")

def test_function():
    queue = [3,4,2,1,3,2,2,2,1,2,3,4,2,1,4,3,4,3,2,1,2,3,1,3,1,]
    for i in queue:
        if i == 1:
            kontrola_wilgotnosci()
        elif i == 2:
            wentyluj_powietrze()
        elif i == 3:
            mieszaj_powietrze()
        elif i == 4:
            get_all_data()
    print("koniec testu")


# === Schedule ===
schedule.every(10).minutes.do(lambda: log_and_display(get_all_data()))
schedule.every(5).minutes.do(kontrola_wilgotnosci)
schedule.every(120).minutes.do(wentyluj_powietrze)
schedule.every(30).minutes.do(mieszaj_powietrze)

# === Główna pętla ===
print("[SZKLARNIA] System uruchomiony.")
while True:
    schedule.run_pending()
    time.sleep(1)
