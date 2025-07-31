from flask import Flask, render_template, jsonify
import csv
import os
app = Flask(__name__)

@app.route('/')
def index():
    timestamps = []
    humidities1 = []
    humidities2 = []

    if os.path.exists("data/log.csv"):
        with open("data/log.csv") as f:
            reader = csv.DictReader(f)
            for row in reader:
                timestamps.append(row["time"])
                humidities1.append(float(row.get("DHT 1_hum", 0)))
                humidities2.append(float(row.get("DHT 2_hum", 0)))

    else:
        print("[APP] Brak pliku log.csv – brak danych do wyświetlenia.")

    return render_template("index.html", timestamps=timestamps, humidities1=humidities1, humidities2=humidities2)

@app.route('/data')
def data():
    timestamps = []
    humidities1 = []
    humidities2 = []

    if os.path.exists("data/log.csv"):
        with open("data/log.csv") as f:
            reader = csv.DictReader(f)
            for row in reader:
                timestamps.append(row["time"])
                humidities1.append(float(row.get("DHT 1_hum", 0)))
                humidities2.append(float(row.get("DHT 2_hum", 0)))

    return jsonify({
        "timestamps": timestamps,
        "humidities1": humidities1,
        "humidities2": humidities2
    })



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
