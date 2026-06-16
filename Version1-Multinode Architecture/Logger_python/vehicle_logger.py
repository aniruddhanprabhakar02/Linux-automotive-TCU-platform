import sqlite3
import paho.mqtt.client as mqtt
import re

# ----------------------------
# SQLite Setup
# ----------------------------

conn = sqlite3.connect("vehicle_telematics.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS location(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    latitude REAL,
    longitude REAL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS status(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    speed INTEGER,
    fuel INTEGER
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS diagnostics(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    rpm INTEGER,
    engine_temp INTEGER
)
""")

conn.commit()

# ----------------------------
# MQTT Callback
# ----------------------------

def on_message(client, userdata, msg):

    payload = msg.payload.decode()

    print(f"\nTopic: {msg.topic}")
    print(f"Payload: {payload}")

    if msg.topic == "vehicle/location":

        lat = float(
            re.search(
                r'Latitude=([\d.]+)',
                payload).group(1)
        )

        lon = float(
            re.search(
                r'Longitude=([\d.]+)',
                payload).group(1)
        )

        cursor.execute(
            "INSERT INTO location(latitude,longitude) VALUES(?,?)",
            (lat, lon)
        )

    elif msg.topic == "vehicle/status":

        speed = int(
            re.search(
                r'Speed=(\d+)',
                payload).group(1)
        )

        fuel = int(
            re.search(
                r'Fuel=(\d+)',
                payload).group(1)
        )

        cursor.execute(
            "INSERT INTO status(speed,fuel) VALUES(?,?)",
            (speed, fuel)
        )

    elif msg.topic == "vehicle/diagnostics":

        rpm = int(
            re.search(
                r'RPM=(\d+)',
                payload).group(1)
        )

        temp = int(
            re.search(
                r'EngineTemp=(\d+)',
                payload).group(1)
        )

        cursor.execute(
            "INSERT INTO diagnostics(rpm,engine_temp) VALUES(?,?)",
            (rpm, temp)
        )

    conn.commit()

# ----------------------------
# MQTT Setup
# ----------------------------

client = mqtt.Client()

client.on_message = on_message

client.connect("localhost", 1883, 60)

client.subscribe("vehicle/location")
client.subscribe("vehicle/status")
client.subscribe("vehicle/diagnostics")

print("Vehicle Logger Started...")

client.loop_forever()
