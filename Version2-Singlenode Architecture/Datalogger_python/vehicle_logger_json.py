import sqlite3
import json
import paho.mqtt.client as mqtt

# -----------------------------
# Database Setup
# -----------------------------

conn = sqlite3.connect(
    "vehicle_telematics_v2.db"
)

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS telematics(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    speed INTEGER,
    rpm INTEGER,
    fuel INTEGER,
    engine_temp INTEGER,
    latitude REAL,
    longitude REAL
)
""")

conn.commit()

# -----------------------------
# MQTT Callback
# -----------------------------

def on_message(client, userdata, msg):

    payload = msg.payload.decode()

    data = json.loads(payload)

    speed = data["speed"]
    rpm = data["rpm"]
    fuel = data["fuel"]
    engine_temp = data["engineTemp"]
    latitude = data["latitude"]
    longitude = data["longitude"]

    cursor.execute(
        """
        INSERT INTO telematics(
            speed,
            rpm,
            fuel,
            engine_temp,
            latitude,
            longitude
        )
        VALUES(?,?,?,?,?,?)
        """,
        (
            speed,
            rpm,
            fuel,
            engine_temp,
            latitude,
            longitude
        )
    )

    conn.commit()

    print(
        f"Logged: "
        f"Speed={speed}, "
        f"RPM={rpm}, "
        f"Fuel={fuel}"
    )

# -----------------------------
# MQTT Setup
# -----------------------------

client = mqtt.Client()

client.on_message = on_message

client.connect(
    "localhost",
    1883,
    60
)

client.subscribe(
    "vehicle/telematics"
)

print(
    "JSON Telematics Logger Started..."
)

client.loop_forever()
