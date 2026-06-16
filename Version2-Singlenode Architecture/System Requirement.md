# System_Requirements.md

# Linux-Automotive-TCU-Platform

## Version 2.0

## Hardware Requirements

### Mandatory

* Raspberry Pi 4B
* MicroSD Card
* Internet Connection

### Optional

* NEO-6M GPS Module
* HC-05 Bluetooth Module

Current Version 2.0 uses software simulation and does not require external hardware.

---

# Operating System

* Raspberry Pi OS (Bookworm Recommended)

---

# Development Tools

Install:

```bash
sudo apt update

sudo apt install build-essential

sudo apt install g++

sudo apt install cmake
```

---

# MQTT Requirements

Install:

```bash
sudo apt install mosquitto

sudo apt install mosquitto-clients

sudo apt install libmosquitto-dev
```

Verify:

```bash
dpkg -l | grep mosquitto
```

---

# SocketCAN Requirements

Install:

```bash
sudo apt install can-utils
```

Verify:

```bash
candump --help
```

---

# SQLite Requirements

Install:

```bash
sudo apt install sqlite3
```

Verify:

```bash
sqlite3 --version
```

---

# JSON Library

Install:

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

# Python Requirements

Python 3.9+ Recommended

Verify:

```bash
python3 --version
```

---

# Python Packages

Install:

```bash
pip3 install -r requirements.txt
```

---

# Virtual CAN Setup

Create vcan0:

```bash
sudo modprobe vcan

sudo ip link add dev vcan0 type vcan

sudo ip link set up vcan0
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

# Software Stack

* C++
* Python
* SocketCAN
* MQTT
* Mosquitto
* SQLite
* Streamlit
* Plotly
* Pandas
* Geopy
* nlohmann/json

---

# Project Components

Backend:

* Vehicle Simulator
* SocketCAN Publisher
* ECU Receiver
* MQTT Publisher
* SQLite Logger

Frontend:

* Streamlit Dashboard
* Instrument Cluster
* Vehicle Alerts
* GPS Route Tracking
* Analytics Dashboard

---

# Current Version

Version 2.0
