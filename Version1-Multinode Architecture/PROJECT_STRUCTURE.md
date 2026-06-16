## Current Project Structure

All project files are stored in the home directory:

```text
/home/aniruddhan/

├── tcu_mqttCAN.cpp
├── ecu_receiver.cpp
├── vehicle_logger.py
├── start_vcan.sh
└── vehicle_telematics.db
```

## File Description

### tcu_mqttCAN.cpp

Main TCU Simulator.

Functions:

* Vehicle Data Generation
* GPS Simulation
* MQTT Publishing
* CAN Frame Transmission

---

### ecu_receiver.cpp

CAN Receiver ECU.

Functions:

* Receive CAN Frames from vcan0
* Decode Vehicle Speed
* Decode RPM
* Decode Engine Temperature

---

### vehicle_logger.py

MQTT Subscriber and SQLite Logger.

Functions:

* Subscribe to MQTT Topics
* Store Location Data
* Store Vehicle Status
* Store Diagnostic Data

---

### start_vcan.sh

Virtual CAN startup script.

Functions:

* Load vcan module
* Create vcan0 interface
* Enable vcan0

---

### vehicle_telematics.db

SQLite database.

Tables:

* location
* status
* diagnostics

Stores all telematics data received from MQTT.

---

## Notes

* All files are kept in the same directory for simplicity during development.
* No additional folder structure is required for Version 1.0.
* Future versions may separate source code, scripts, logs, and database files into dedicated folders.

## Version

Version 1.0

Architecture:

* 1 MQTT Publisher
* 3 MQTT Subscribers
* 1 CAN Receiver
* SQLite Logger
* SocketCAN (vcan0)
* Raspberry Pi 4B
