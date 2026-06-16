# Linux-Automotive-TCU-Platform

## Version 2.0

A Linux-based Automotive Telematics Control Unit (TCU) Simulator developed on Raspberry Pi 4B using C++, SocketCAN, MQTT, JSON, SQLite, and Streamlit.

The project simulates a real-world automotive telematics architecture by generating vehicle telemetry, transmitting data over CAN and MQTT, logging telemetry into SQLite, and visualizing vehicle status through a live dashboard.

---

# Features

## Vehicle Simulation

Simulated vehicle parameters:

* Vehicle Speed
* Engine RPM
* Fuel Level
* Engine Temperature
* GPS Coordinates

Vehicle telemetry is generated continuously every second.

---

## SocketCAN Communication

Virtual CAN interface:

```text
vcan0
```

CAN IDs:

| CAN ID | Signal             |
| ------ | ------------------ |
| 0x100  | Vehicle Speed      |
| 0x101  | Engine RPM         |
| 0x102  | Engine Temperature |

An ECU Receiver node listens on the CAN network and decodes incoming CAN frames.

---

## MQTT Communication

MQTT Broker:

```text
Mosquitto
```

Single MQTT Topic:

```text
vehicle/telematics
```

Vehicle telemetry is transmitted as a JSON payload.

Example:

```json
{
  "latitude": 13.0828,
  "longitude": 80.2708,
  "speed": 84,
  "rpm": 5523,
  "fuel": 17,
  "engineTemp": 94
}
```

---

## SQLite Data Logging

Database:

```text
vehicle_telematics_v2.db
```

Table:

```sql
telematics
(
 id,
 timestamp,
 speed,
 rpm,
 fuel,
 engine_temp,
 latitude,
 longitude
)
```

All MQTT telemetry packets are stored automatically.

---

## Streamlit Dashboard

Real-time dashboard capabilities:

### Instrument Cluster

* Speed Gauge
* RPM Gauge
* Fuel Gauge
* Engine Temperature Gauge

### Vehicle Monitoring

* Vehicle Health Status
* Overspeed Detection
* High RPM Detection
* Low Fuel Detection
* Engine Overheating Detection

### GPS Monitoring

* Live GPS Coordinates
* Current Vehicle Position
* Historical Route Tracking

### Historical Telemetry

* Speed vs Time
* RPM vs Time
* Fuel vs Time
* Engine Temperature vs Time

### Analytics Dashboard

* Total Records
* Average Speed
* Maximum RPM
* Average Fuel
* Maximum Engine Temperature
* Distance Travelled Estimation

---

# System Architecture

```text
Vehicle Simulator (C++)
       |
       v
SocketCAN (vcan0)
       |
       v
ECU Receiver
       |
       v
Mosquitto MQTT Broker
       |
       v
JSON Telemetry
(vehicle/telematics)
       |
       v
vehicle_logger_json.py
       |
       v
vehicle_telematics_v2.db
       |
       v
TCU_dashboard_v3.py
       |
       +---- Instrument Cluster
       +---- Vehicle Alerts
       +---- GPS Tracking
       +---- Analytics Dashboard
       +---- Historical Charts
```

---

# Project Files

```text
/home/aniruddhan/

├── tcu_1publisher_mqttCAN.cpp
├── ecu_receiver.cpp
├── vehicle_logger_json.py
├── TCU_dashboard_v3.py
├── start_vcan.sh
└── vehicle_telematics_v2.db
```

---

# Technologies Used

### Embedded Software

* C++
* Python

### Communication Protocols

* MQTT
* SocketCAN

### Linux Components

* Mosquitto Broker
* Virtual CAN (vcan0)

### Database

* SQLite

### Dashboard Framework

* Streamlit
* Plotly

### Data Processing

* Pandas
* Geopy

### JSON Serialization

* nlohmann/json

---

# Software Requirements

### Linux Packages

```bash
sudo apt update

sudo apt install build-essential
sudo apt install g++
sudo apt install cmake

sudo apt install mosquitto
sudo apt install mosquitto-clients
sudo apt install libmosquitto-dev

sudo apt install can-utils

sudo apt install sqlite3

sudo apt install nlohmann-json3-dev
```

### Python Packages

```bash
pip3 install paho-mqtt

pip3 install streamlit

pip3 install pandas

pip3 install plotly

pip3 install streamlit-autorefresh

pip3 install geopy
```

---

# Running the Project

## Terminal 1

Start Virtual CAN:

```bash
./start_vcan.sh
```

---

## Terminal 2

Start ECU Receiver:

```bash
./ecu_receiver
```

---

## Terminal 3

Start SQLite Logger:

```bash
python3 vehicle_logger_json.py
```

---

## Terminal 4

Start TCU Simulator:

```bash
./tcu_1publisher_mqttCAN
```

---

## Terminal 5

Start Dashboard:

```bash
streamlit run TCU_dashboard_v3.py
```

Open:

```text
http://localhost:8501
```

---

# Analytics Available

The dashboard automatically calculates:

* Total Telemetry Records
* Average Vehicle Speed
* Maximum RPM
* Average Fuel Level
* Maximum Engine Temperature
* Distance Travelled

Distance is estimated using GPS coordinates and geodesic calculations.

---

# Current Project Status

| Module              | Status |
| ------------------- | ------ |
| Vehicle Simulator   | ✅      |
| GPS Simulation      | ✅      |
| SocketCAN           | ✅      |
| ECU Receiver        | ✅      |
| MQTT Broker         | ✅      |
| JSON Telemetry      | ✅      |
| SQLite Logging      | ✅      |
| Streamlit Dashboard | ✅      |
| Instrument Cluster  | ✅      |
| Vehicle Alerts      | ✅      |
| GPS Tracking        | ✅      |
| Analytics Dashboard | ✅      |
| Historical Charts   | ✅      |

---