# Linux-Based Automotive Telematics Control Unit (TCU) Simulator

## Project Overview

This project implements a software-defined Automotive Telematics Control Unit (TCU) on a Raspberry Pi 4B running Linux.

The objective is to simulate key telematics and vehicle networking functionalities used in modern connected vehicles, including:

* Vehicle telemetry generation
* GPS tracking
* MQTT-based cloud communication
* CAN bus communication using SocketCAN
* ECU-to-ECU communication
* Data logging using SQLite
* Linux networking and embedded software development

The project is implemented using C++, Python, MQTT, SocketCAN, and SQLite.

---

# Hardware Platform

## Mandatory Hardware

* Raspberry Pi 4B
* MicroSD Card
* Internet Connection

## Optional Hardware

* NEO-6M GPS Module
* HC-05 Bluetooth Module

The current implementation is fully software-based and does not require external GPS or Bluetooth hardware.

---

# Software Environment

## Operating System

* Raspberry Pi OS (Bookworm)

## Development Language

* C++
* Python 3

---

# Required Packages

```bash
sudo apt update

sudo apt install build-essential
sudo apt install cmake

sudo apt install mosquitto
sudo apt install mosquitto-clients
sudo apt install libmosquitto-dev

sudo apt install can-utils

sudo apt install gpsd gpsd-clients
sudo apt install libgps-dev

sudo apt install bluetooth

sudo apt install sqlite3
```

Python package:

```bash
pip3 install paho-mqtt
```

---

# System Architecture

```text
                     MQTT Subscribers
                            ^
                            |
                      Mosquitto Broker
                            ^
                            |
                      MQTT Publisher
                            ^
                            |
+--------------------------------------------------+
| Raspberry Pi 4B                                  |
|                                                  |
| Vehicle Data Generator                           |
| GPS Simulator                                    |
| MQTT Publisher                                   |
| CAN Publisher                                    |
| SQLite Logger                                    |
+--------------------------------------------------+
               |
               v
             vcan0
               |
               v
        ECU Receiver Node
```

---

# Implemented Features

## Phase 1 – Vehicle Simulator

Simulated vehicle parameters:

* Vehicle Speed
* Engine RPM
* Fuel Level
* Engine Temperature

Example:

```cpp
speed = rand() % 120;
rpm = rand() % 6000;
fuel = rand() % 100;
engineTemp = 70 + rand() % 40;
```

---

## Phase 2 – GPS Simulator

GPS coordinates are generated in software.

Initial coordinates:

```text
Latitude  = 13.0827
Longitude = 80.2707
```

Vehicle movement simulation:

```cpp
gps.latitude += 0.0001;
gps.longitude += 0.0001;
```

---

## Phase 3 – MQTT Integration

### MQTT Topics

| Topic               | Data                    |
| ------------------- | ----------------------- |
| vehicle/location    | Latitude, Longitude     |
| vehicle/status      | Speed, Fuel             |
| vehicle/diagnostics | RPM, Engine Temperature |

### MQTT Architecture

```text
TCU Simulator
      |
      v
Mosquitto Broker
      |
+-----+-----+-----+
|           |     |
v           v     v
Location  Status Diagnostics
```

### Publisher

The C++ TCU publishes telemetry data every second.

### Subscribers

Three MQTT subscribers receive data independently:

```bash
mosquitto_sub -h localhost -t vehicle/location

mosquitto_sub -h localhost -t vehicle/status

mosquitto_sub -h localhost -t vehicle/diagnostics
```

---

## Phase 4 – SocketCAN Integration

Linux Virtual CAN interface:

```text
vcan0
```

### CAN IDs

| CAN ID | Signal             |
| ------ | ------------------ |
| 0x100  | Vehicle Speed      |
| 0x101  | Engine RPM         |
| 0x102  | Engine Temperature |

### Create Virtual CAN Interface

```bash
sudo modprobe vcan

sudo ip link add dev vcan0 type vcan

sudo ip link set up vcan0
```

### Monitor CAN Traffic

```bash
candump vcan0
```

---

## CAN Frame Example

```text
vcan0 100 [1] 4F
vcan0 101 [2] 0F 74
vcan0 102 [1] 52
```

Decoded values:

```text
Speed       = 79 km/h
RPM         = 3956
Temperature = 82 °C
```

---

## Phase 4.1 – ECU Receiver

An independent ECU node was developed to receive and decode CAN messages.

Architecture:

```text
TCU Simulator
      |
      v
    vcan0
      |
      v
ECU Receiver
```

Decoded Signals:

* Speed
* RPM
* Engine Temperature

Example Output:

```text
Received Speed       : 57 km/h
Received RPM         : 5604
Received Temperature : 98 C
```

---

## Phase 5A – SQLite Logger

A Python MQTT logger subscribes to MQTT topics and stores data in SQLite.

### Database

```text
vehicle_telematics.db
```

### Tables

#### location

```sql
id
timestamp
latitude
longitude
```

#### status

```sql
id
timestamp
speed
fuel
```

#### diagnostics

```sql
id
timestamp
rpm
engine_temp
```

### Data Flow

```text
TCU Publisher
      |
      v
Mosquitto Broker
      |
      v
vehicle_logger.py
      |
      v
SQLite Database
```

---

# Current System Status

| Feature              | Status |
| -------------------- | ------ |
| Vehicle Simulation   | ✅      |
| GPS Simulation       | ✅      |
| MQTT Broker          | ✅      |
| MQTT Publishing      | ✅      |
| MQTT Subscribers     | ✅      |
| SocketCAN            | ✅      |
| CAN Transmission     | ✅      |
| CAN Reception        | ✅      |
| ECU Receiver Node    | ✅      |
| SQLite Logger        | ✅      |
| Linux Networking     | ✅      |
| Telematics Data Flow | ✅      |

---

# Current Version

## Version 1.0

Architecture:

```text
1 Publisher
3 MQTT Subscribers
1 CAN Receiver
1 SQLite Logger
```

Implemented Technologies:

* C++
* Python
* MQTT
* SocketCAN
* SQLite
* Embedded Linux
* Raspberry Pi 4B

---

# Future Work

* Unified MQTT Subscriber
* Instrument Cluster Dashboard
* Node-RED Dashboard
* TCP Diagnostic Server
* GPS Hardware Integration
* Bluetooth Services
* Systemd Service Deployment
* OTA Update Framework
* Real CAN Hardware Integration
