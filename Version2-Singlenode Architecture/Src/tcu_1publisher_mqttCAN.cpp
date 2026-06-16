#include <iostream>
#include <cstdlib>
#include <ctime>
#include <unistd.h>
#include <cstring>

#include <mosquitto.h>

#include <nlohmann/json.hpp>

// CAN headers
#include <linux/can.h>
#include <linux/can/raw.h>

#include <sys/socket.h>
#include <sys/ioctl.h>

#include <net/if.h>

using json = nlohmann::json;

struct GPSData
{
    double latitude;
    double longitude;
};

struct VehicleData
{
    int speed;
    int rpm;
    int fuel;
    int engineTemp;
    GPSData gps;
};

int main()
{
    srand(time(NULL));

    VehicleData vehicle;

    vehicle.gps.latitude = 13.0827;
    vehicle.gps.longitude = 80.2707;

    // MQTT Initialization
    mosquitto_lib_init();

    struct mosquitto *mosq =
        mosquitto_new("TCU_Client", true, NULL);

    if(!mosq)
    {
        std::cerr << "Failed to create MQTT client\n";
        return 1;
    }

    if(mosquitto_connect(
           mosq,
           "localhost",
           1883,
           60) != MOSQ_ERR_SUCCESS)
    {
        std::cerr << "Failed to connect to broker\n";

        mosquitto_destroy(mosq);
        mosquitto_lib_cleanup();

        return 1;
    }

    std::cout << "Connected to MQTT Broker\n";

    // --------------------------------------------------
    // CAN Socket Initialization
    // --------------------------------------------------

    int can_socket;

    struct sockaddr_can addr;
    struct ifreq ifr;

    can_socket =
        socket(PF_CAN,
               SOCK_RAW,
               CAN_RAW);

    strcpy(ifr.ifr_name, "vcan0");

    ioctl(can_socket,
          SIOCGIFINDEX,
          &ifr);

    addr.can_family = AF_CAN;
    addr.can_ifindex = ifr.ifr_ifindex;

    bind(can_socket,
         (struct sockaddr *)&addr,
         sizeof(addr));

    std::cout << "Connected to vcan0\n";

    while(true)
    {
        // -----------------------------------------
        // Generate Vehicle Data
        // -----------------------------------------

        vehicle.speed = rand() % 120;
        vehicle.rpm = rand() % 6000;
        vehicle.fuel = rand() % 100;
        vehicle.engineTemp =
            80 + rand() % 21;

        // -----------------------------------------
        // CAN Frames
        // -----------------------------------------

        struct can_frame speedFrame;
        struct can_frame rpmFrame;
        struct can_frame tempFrame;

        // Speed Frame (0x100)

        speedFrame.can_id = 0x100;
        speedFrame.can_dlc = 1;

        speedFrame.data[0] =
            vehicle.speed;

        // RPM Frame (0x101)

        rpmFrame.can_id = 0x101;
        rpmFrame.can_dlc = 2;

        rpmFrame.data[0] =
            (vehicle.rpm >> 8) & 0xFF;

        rpmFrame.data[1] =
            vehicle.rpm & 0xFF;

        // Temperature Frame (0x102)

        tempFrame.can_id = 0x102;
        tempFrame.can_dlc = 1;

        tempFrame.data[0] =
            vehicle.engineTemp;

        // -----------------------------------------
        // Send CAN Frames
        // -----------------------------------------

        write(can_socket,
              &speedFrame,
              sizeof(speedFrame));

        write(can_socket,
              &rpmFrame,
              sizeof(rpmFrame));

        write(can_socket,
              &tempFrame,
              sizeof(tempFrame));

        // -----------------------------------------
        // GPS Simulation
        // -----------------------------------------

        vehicle.gps.latitude += 0.0001;
        vehicle.gps.longitude += 0.0001;

        // -----------------------------------------
        // Create JSON Telemetry Packet
        // -----------------------------------------

        json telemetry;
        //nlohmann::json telemetry;

        telemetry["latitude"] =
            vehicle.gps.latitude;

        telemetry["longitude"] =
            vehicle.gps.longitude;

        telemetry["speed"] =
            vehicle.speed;

        telemetry["rpm"] =
            vehicle.rpm;

        telemetry["fuel"] =
            vehicle.fuel;

        telemetry["engineTemp"] =
            vehicle.engineTemp;

        std::string payload =
            telemetry.dump();

        // -----------------------------------------
        // Publish MQTT
        // -----------------------------------------

        mosquitto_publish(
            mosq,
            NULL,
            "vehicle/telematics",
            payload.length(),
            payload.c_str(),
            0,
            false);

        // -----------------------------------------
        // Console Output
        // -----------------------------------------

        std::cout
            << "\n==============================\n";

        std::cout
            << "Vehicle Telemetry\n";

        std::cout
            << "==============================\n";

        std::cout
            << "Latitude     : "
            << vehicle.gps.latitude
            << std::endl;

        std::cout
            << "Longitude    : "
            << vehicle.gps.longitude
            << std::endl;

        std::cout
            << "Speed        : "
            << vehicle.speed
            << " km/h"
            << std::endl;

        std::cout
            << "RPM          : "
            << vehicle.rpm
            << std::endl;

        std::cout
            << "Fuel         : "
            << vehicle.fuel
            << "%"
            << std::endl;

        std::cout
            << "Engine Temp  : "
            << vehicle.engineTemp
            << " C"
            << std::endl;

        std::cout
            << "\nJSON Payload:\n"
            << payload
            << std::endl;

        sleep(1);
    }

    // Cleanup

    mosquitto_disconnect(mosq);
    mosquitto_destroy(mosq);
    mosquitto_lib_cleanup();

    return 0;
}
