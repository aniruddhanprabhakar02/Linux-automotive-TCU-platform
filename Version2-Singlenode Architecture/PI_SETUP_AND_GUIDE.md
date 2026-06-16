# PI_SETUP_AND_GUIDE.md

# Raspberry Pi 4B Setup and Execution Guide

This guide explains how to set up the Raspberry Pi environment and run the Linux Automotive TCU Platform.

---

# Hardware Used

* Raspberry Pi 4B
* MicroSD Card
* Internet Connection

Optional:

* GPS Module
* Bluetooth Module

This project currently uses software simulation and does not require external hardware.

---

# Update Raspberry Pi

```bash
sudo apt update
sudo apt upgrade -y
```

---

# Install Development Tools

```bash
sudo apt install build-essential

sudo apt install g++

sudo apt install cmake
```

Verify:

```bash
g++ --version
```

---

# Install MQTT

```bash
sudo apt install mosquitto

sudo apt install mosquitto-clients

sudo apt install libmosquitto-dev
```

Verify:

```bash
dpkg -l | grep mosquitto
```

Expected packages:

```text
mosquitto
mosquitto-clients
libmosquitto-dev
```

---

# Install SocketCAN Utilities

```bash
sudo apt install can-utils
```

Verify:

```bash
candump --help
```

---

# Install SQLite

```bash
sudo apt install sqlite3
```

Verify:

```bash
sqlite3 --version
```

---

# Install JSON Library

```bash
sudo apt install nlohmann-json3-dev
```

Verify:

```bash
ls /usr/include/nlohmann/json.hpp
```

Expected:

```text
/usr/include/nlohmann/json.hpp
```

---

# Install Python Packages

```bash
pip3 install paho-mqtt

pip3 install streamlit

pip3 install pandas

pip3 install plotly

pip3 install streamlit-autorefresh

pip3 install geopy
```

Verify:

```bash
pip3 list
```

---

# Create Virtual CAN Startup Script

Create file:

```bash
nano start_vcan.sh
```

Paste:

```bash
#!/bin/bash

sudo modprobe vcan

sudo ip link add dev vcan0 type vcan 2>/dev/null

sudo ip link set up vcan0
```

Save:

```text
CTRL + O
ENTER
CTRL + X
```

Make executable:

```bash
chmod +x start_vcan.sh
```

---

# Create Source Files

Create:

```bash
nano tcu_1publisher_mqttCAN.cpp
```

Paste project source code.

Save:

```text
CTRL + O
ENTER
CTRL + X
```

---

Create:

```bash
nano ecu_receiver.cpp
```

Paste project source code.

Save:

```text
CTRL + O
ENTER
CTRL + X
```

---

Create:

```bash
nano vehicle_logger_json.py
```

Paste project source code.

Save:

```text
CTRL + O
ENTER
CTRL + X
```

---

Create:

```bash
nano TCU_dashboard_v3.py
```

Paste project source code.

Save:

```text
CTRL + O
ENTER
CTRL + X
```

---

# Compile C++ Applications

## Compile TCU Simulator

```bash
g++ tcu_1publisher_mqttCAN.cpp \
-o tcu_1publisher_mqttCAN \
-lmosquitto \
-std=c++17
```

---

## Compile ECU Receiver

```bash
g++ ecu_receiver.cpp \
-o ecu_receiver
```

---

# Verify Executables

```bash
ls
```

Expected:

```text
tcu_1publisher_mqttCAN
ecu_receiver
```

---

# Project Execution

Open 5 terminals.

---

# Terminal 1

Start Virtual CAN:

```bash
./start_vcan.sh
```

Verify:

```bash
ip link show vcan0
```

Expected:

```text
vcan0: <NOARP,UP,LOWER_UP>
```

---

# Terminal 2

Start ECU Receiver:

```bash
./ecu_receiver
```

Expected:

```text
ECU Receiver Listening on vcan0...
```

---

# Terminal 3

Start MQTT Logger:

```bash
python3 vehicle_logger_json.py
```

Expected:

```text
JSON Telematics Logger Started...
```

---

# Terminal 4

Start TCU Simulator:

```bash
./tcu_1publisher_mqttCAN
```

Expected:

```text
Connected to MQTT Broker

Connected to vcan0
```

Vehicle telemetry should begin printing every second.

---

# Terminal 5

Launch Dashboard:

```bash
streamlit run TCU_dashboard_v3.py
```

Expected:

```text
Local URL:

http://localhost:8501
```

Open:

```text
http://localhost:8501
```

in a web browser.

---

# Verify MQTT Telemetry

Open an additional terminal:

```bash
mosquitto_sub -h localhost -t vehicle/telematics
```

Expected:

```json
{
  "latitude":13.0828,
  "longitude":80.2708,
  "speed":84,
  "rpm":5523,
  "fuel":17,
  "engineTemp":94
}
```

---

# Verify CAN Traffic

Open an additional terminal:

```bash
candump vcan0
```

Expected:

```text
vcan0 100 [1] 4F
vcan0 101 [2] 0F 74
vcan0 102 [1] 52
```

---

# Verify SQLite Database

Open SQLite:

```bash
sqlite3 vehicle_telematics_v2.db
```

Show tables:

```sql
.tables
```

Expected:

```text
telematics
```

View records:

```sql
SELECT * FROM telematics LIMIT 5;
```

Example:

```text
1|2026-06-13 07:27:32|84|5523|17|94|13.0828|80.2708
2|2026-06-13 07:27:33|57|459|75|99|13.0829|80.2709
```

---

# Dashboard Features

## Instrument Cluster

* Speed Gauge
* RPM Gauge
* Fuel Gauge
* Engine Temperature Gauge

## Vehicle Alerts

* Engine Overheating
* Low Fuel
* High RPM
* Overspeed

## GPS Tracking

* Live Vehicle Position
* Route Visualization

## Analytics Dashboard

* Total Records
* Average Speed
* Maximum RPM
* Average Fuel
* Maximum Temperature
* Distance Travelled

## Historical Charts

* Speed History
* RPM History
* Fuel History
* Engine Temperature History

---

# Troubleshooting

## vcan0 Not Found

Run:

```bash
./start_vcan.sh
```

again.

---

## MQTT Connection Failed

Check broker:

```bash
sudo systemctl status mosquitto
```

Start broker:

```bash
sudo systemctl start mosquitto
```

---

## Dashboard Not Opening

Verify Streamlit:

```bash
streamlit --version
```

Run:

```bash
streamlit run TCU_dashboard_v3.py
```

Open:

```text
http://localhost:8501
```

---

# Project Status

Current Version:

```text
Version 2.0
```

Implemented:

```text
Vehicle Simulator           ✓
SocketCAN                   ✓
MQTT                        ✓
JSON Telemetry              ✓
SQLite Logging              ✓
Streamlit Dashboard         ✓
Instrument Cluster          ✓
Vehicle Alerts              ✓
GPS Route Tracking          ✓
Analytics Dashboard         ✓
```
