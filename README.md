# Linux-Automotive-TCU-Platform

## Overview

Linux-Automotive-TCU-Platform is a Linux-based Automotive Telematics Control Unit (TCU) simulator developed on Raspberry Pi 4B.

The project demonstrates the core technologies commonly used in connected vehicle systems:

* Embedded Linux
* SocketCAN
* MQTT
* JSON Telemetry
* SQLite
* Streamlit Dashboard
* Vehicle Diagnostics
* GPS Tracking
* Real-Time Data Visualization

The repository contains two implementations of the TCU platform.

---

# Repository Structure

```text
Linux-Automotive-TCU-Platform/

├── Version_1/
│
├── Version_2/
│
├── README.md
├── .gitignore

```

---

# Version 1

## Architecture

```text
Vehicle Simulator
        |
        +---- MQTT
        |
        +---- CAN
```

### Features

* Vehicle Data Simulation
* GPS Simulation
* SocketCAN Communication
* MQTT Telemetry
* ECU Receiver
* SQLite Logging
* Streamlit Dashboard

### MQTT Topics

```text
vehicle/location

vehicle/status

vehicle/diagnostics
```

### SQLite Tables

```text
location

status

diagnostics
```

---

# Version 2

## Architecture

```text
Vehicle Simulator
        |
        +---- CAN
        |
        +---- MQTT JSON
```

### Features

* Vehicle Data Simulation
* GPS Simulation
* SocketCAN Communication
* ECU Receiver
* JSON Telemetry
* SQLite Logging
* Instrument Cluster
* Vehicle Alerts
* GPS Route Tracking
* Analytics Dashboard

### MQTT Topic

```text
vehicle/telematics
```

### JSON Payload

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

### SQLite Table

```text
telematics
```

---

# System Architecture

```text
Vehicle Simulator (C++)
          |
          +---- SocketCAN ----> ECU Receiver
          |
          +---- MQTT Telemetry
                      |
                      v
               Mosquitto Broker
                      |
                      v
                SQLite Logger
                      |
                      v
                 SQLite DB
                      |
                      v
             Streamlit Dashboard
```

---

# Technologies Used

## Backend

* C++
* Python
* SocketCAN
* Mosquitto MQTT
* SQLite
* nlohmann/json

## Frontend

* Streamlit
* Plotly
* Pandas

## Analytics

* Geopy
* SQLite Queries

---

# Hardware Platform

* Raspberry Pi 4B
* MicroSD Card
* Internet Connection

Optional:

* GPS Module
* Bluetooth Module

Current implementations use software simulation and do not require external hardware.

---

# Key Learning Areas

This project demonstrates:

* Automotive Telematics
* CAN Communication
* Linux Networking
* MQTT Messaging
* JSON Data Serialization
* Database Logging
* Real-Time Dashboards
* GPS Tracking
* Vehicle Analytics
* Embedded Linux Development

---

# Documentation

Refer to the version-specific folders for:

* Setup Instructions
* Source Code
* Project Structure
* Dashboard Screenshots
* Execution Guides

---

# Current Status

## Version 1

Completed:

* Vehicle Simulator
* GPS Simulation
* SocketCAN
* MQTT (3 Topics)
* ECU Receiver
* SQLite Logging
* Streamlit Dashboard

## Version 2

Completed:

* Vehicle Simulator
* GPS Simulation
* SocketCAN
* MQTT JSON Telemetry
* ECU Receiver
* SQLite Logging
* Instrument Cluster
* Vehicle Alerts
* GPS Route Tracking
* Analytics Dashboard

---

# Author

Aniruddhan P

Linux-Based Automotive Telematics Control Unit (TCU) Platform on Raspberry Pi.
