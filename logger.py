import csv
from datetime import datetime
import os

LOG_FILE = "data/log.csv"

def log_and_display(x):
    data = x
    print("\n[LOG DANYCH]")
    for entry in data:
        if entry["type"] == "DHT":
            print(f"{entry['id']}: Temp={entry['temp']:.1f}C, Wilg={entry['hum']:.1f}%")
        elif entry["type"] == "TSL":
            print(f"{entry['id']}: Lux={entry['lux']:.1f}")

    # Zapis do pliku CSV
    row = {"time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    for entry in data:
        if entry["type"] == "DHT":
            row[f"{entry['id']}_temp"] = round(entry["temp"], 1)
            row[f"{entry['id']}_hum"] = round(entry["hum"], 1)
        elif entry["type"] == "TSL":
            row[f"{entry['id']}_lux"] = round(entry["lux"], 1)

    file_exists = os.path.isfile(LOG_FILE)
    with open(LOG_FILE, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=row.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)
