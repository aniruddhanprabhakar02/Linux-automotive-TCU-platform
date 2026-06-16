# Linux Automotive TCU Platform

## Raspberry Pi 4B Setup and Run Guide

---

# 1. Install Required Packages

Update package list:

```bash
sudo apt update
```

Install C++ compiler:

```bash
sudo apt install build-essential
sudo apt install g++
sudo apt install cmake
```

Install MQTT Broker:

```bash
sudo apt install mosquitto
sudo apt install mosquitto-clients
sudo apt install libmosquitto-dev
```

Install SocketCAN utilities:

```bash
sudo apt install can-utils
```

Install SQLite:

```bash
sudo apt install sqlite3
```

Install Python MQTT package:

```bash
pip3 install paho-mqtt
```

---

# 2. Create Source Files

Create TCU Publisher:

```bash
nano tcu_mqttCAN.cpp
```

Paste source code.

Save:

```text
CTRL + O
ENTER
CTRL + X
```

---

Create ECU Receiver:

```bash
nano ecu_receiver.cpp
```

Paste source code.

Save:

```text
CTRL + O
ENTER
CTRL + X
```

---

Create SQLite Logger:

```bash
nano vehicle_logger.py
```

Paste source code.

Save:

```text
CTRL + O
ENTER
CTRL + X
```

---

Create Virtual CAN Startup Script:

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

# 3. Compile Programs

Compile TCU Publisher:

```bash
g++ tcu_mqttCAN.cpp -o tcu_mqttCAN -lmosquitto
```

Compile ECU Receiver:

```bash
g++ ecu_receiver.cpp -o ecu_receiver
```

Verify files:

```bash
ls
```

Expected:

```text
tcu_mqttCAN
ecu_receiver
vehicle_logger.py
start_vcan.sh
```

---

# 4. Setup Virtual CAN

Run:

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

# 5. Run Complete System

Open FIVE terminals.

---

## Terminal 1

Start Virtual CAN

```bash
./start_vcan.sh
```

---

## Terminal 2

Start ECU Receiver

```bash
./ecu_receiver
```

Expected:

```text
ECU Receiver Listening on vcan0...
```

---

## Terminal 3

Start SQLite Logger

```bash
python3 vehicle_logger.py
```

Expected:

```text
Vehicle Logger Started...
```

---

## Terminal 4

Start MQTT Subscriber

Location:

```bash
mosquitto_sub -h localhost -t vehicle/location
```

OR

Status:

```bash
mosquitto_sub -h localhost -t vehicle/status
```

OR

Diagnostics:

```bash
mosquitto_sub -h localhost -t vehicle/diagnostics
```

---

## Terminal 5

Start TCU Publisher

```bash
./tcu_mqttCAN
```

Expected:

```text
Connected to MQTT Broker
Connected to vcan0

----- Vehicle Data -----
Latitude     : 13.0828
Longitude    : 80.2708
Speed        : 75 km/h
RPM          : 4200
Fuel         : 60%
Engine Temp  : 92 C
CAN TX -> 0x100(Speed) 0x101(RPM) 0x102(Temp)
```

---

# 6. Verify CAN Communication

Open another terminal:

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

# 7. Verify SQLite Database

Open SQLite:

```bash
sqlite3 vehicle_telematics.db
```

Show tables:

```sql
.tables
```

Expected:

```text
diagnostics
location
status
```

View records:

```sql
SELECT * FROM location LIMIT 5;

SELECT * FROM status LIMIT 5;

SELECT * FROM diagnostics LIMIT 5;
```

Exit SQLite:

```sql
.quit
```

---

# Project Architecture

```text
Vehicle Data Generator
        |
        +------ MQTT ------> Mosquitto Broker
        |                          |
        |                          +---- vehicle/location
        |                          +---- vehicle/status
        |                          +---- vehicle/diagnostics
        |                          |
        |                          +---- SQLite Logger
        |
        +------ CAN -------> vcan0
                                   |
                                   v
                             ECU Receiver
```

---

# Version

Version 1.0

Architecture:

1 Publisher
3 MQTT Subscribers
1 CAN Receiver
1 SQLite Logger

Platform:

Raspberry Pi 4B
Linux
MQTT
SocketCAN
SQLite
C++
Python
