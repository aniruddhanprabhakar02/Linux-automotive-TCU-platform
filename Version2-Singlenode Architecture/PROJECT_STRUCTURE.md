# PROJECT_STRUCTURE.md

# Linux-Automotive-TCU-Platform

## Version 2.0 Project Structure

All project files are currently stored in:

```text
/home/aniruddhan/
```

Directory Layout:

```text
/home/aniruddhan/

├── tcu_1publisher_mqttCAN.cpp
├── tcu_1publisher_mqttCAN
│
├── ecu_receiver.cpp
├── ecu_receiver
│
├── vehicle_logger_json.py
│
├── TCU_dashboard_v3.py
│
├── start_vcan.sh
│
├── vehicle_telematics_v2.db

```

---

# File Description

## tcu_1publisher_mqttCAN.cpp

Main Automotive TCU Simulator.

Functions:

* Vehicle Data Simulation
* GPS Simulation
* SocketCAN Transmission
* MQTT JSON Telemetry Publishing

Publishes:

```text
vehicle/telematics
```

---

## tcu_1publisher_mqttCAN

Compiled executable generated from:

```text
tcu_1publisher_mqttCAN.cpp
```

Run:

```bash
./tcu_1publisher_mqttCAN
```

---

## ecu_receiver.cpp

Virtual ECU Receiver.

Functions:

* Receive CAN Frames
* Decode Speed
* Decode RPM
* Decode Engine Temperature

Reads data from:

```text
vcan0
```

---

## ecu_receiver

Compiled executable generated from:

```text
ecu_receiver.cpp
```

Run:

```bash
./ecu_receiver
```

---

## vehicle_logger_json.py

MQTT Subscriber and SQLite Logger.

Functions:

* Subscribe to MQTT Telemetry
* Parse JSON Payload
* Store Telemetry in SQLite Database

MQTT Topic:

```text
vehicle/telematics
```

---

## TCU_dashboard_v3.py

Streamlit Dashboard Application.

Features:

* Instrument Cluster
* Vehicle Alerts
* GPS Route Tracking
* Historical Charts
* Analytics Dashboard

Run:

```bash
streamlit run TCU_dashboard_v3.py
```

---

## start_vcan.sh

Virtual CAN startup script.

Functions:

* Load vcan module
* Create vcan0 interface
* Enable vcan0

Run:

```bash
./start_vcan.sh
```

---

## vehicle_telematics_v2.db

SQLite Database.

Table:

```text
telematics
```

Stores:

* Speed
* RPM
* Fuel
* Engine Temperature
* Latitude
* Longitude
* Timestamp


# Runtime Architecture

```text
tcu_1publisher_mqttCAN
            |
            v
        SocketCAN
         (vcan0)
            |
            v
      ecu_receiver

            |

            v

      Mosquitto Broker
            |
            v
    vehicle/telematics
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

Current Version:

```text
Version 2.0
```
