# System Requirements

## Hardware

* Raspberry Pi 4B
* MicroSD Card
* Internet Connection

---

## Operating System

* Raspberry Pi OS Bookworm

---

## Development Tools
apt packages(Linux packages) cannot be installed directly from requirements.txt.

```bash
sudo apt update

sudo apt install build-essential

sudo apt install g++

sudo apt install cmake
```

---

## MQTT

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

## SocketCAN

```bash
sudo apt install can-utils
```

Verify:

```bash
candump --help
```

---

## SQLite

```bash
sudo apt install sqlite3
```

Verify:

```bash
sqlite3 --version
```

---

## Python Packages

Install:

```bash
pip3 install -r requirements.txt
```

Current Python packages:

```text
paho-mqtt
```

---

## Virtual CAN Setup

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
