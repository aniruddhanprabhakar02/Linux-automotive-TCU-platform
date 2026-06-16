#include <iostream>
#include <cstdlib>
#include <ctime>
#include <unistd.h>
#include <cstring>
#include <mosquitto.h>

//CAN headers
#include <linux/can.h>
#include <linux/can/raw.h>

#include <sys/socket.h>
#include <sys/ioctl.h>

#include <net/if.h>


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

   if(mosquitto_connect(mosq,
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



//CAN Socket Initialization

int can_socket;

struct sockaddr_can addr;
struct ifreq ifr;

can_socket = socket(PF_CAN, SOCK_RAW, CAN_RAW);

strcpy(ifr.ifr_name, "vcan0");

ioctl(can_socket, SIOCGIFINDEX, &ifr);

addr.can_family = AF_CAN;
addr.can_ifindex = ifr.ifr_ifindex;

bind(can_socket,
     (struct sockaddr *)&addr,
     sizeof(addr));

std::cout << "Connected to vcan0\n";





   while(true)
   {
       vehicle.speed = rand() % 120;
       vehicle.rpm = rand() % 6000;
       vehicle.fuel = rand() % 100;
       vehicle.engineTemp = 80 + rand() % 21;
      
       struct can_frame speedFrame;
       struct can_frame rpmFrame;
       struct can_frame tempFrame;
       
    // -----------------------------
    // CAN Speed Frame (ID 0x100)
    // -----------------------------
    speedFrame.can_id = 0x100;
    speedFrame.can_dlc = 1;

    speedFrame.data[0] = vehicle.speed;

    // -----------------------------
    // CAN RPM Frame (ID 0x101)
    // -----------------------------
    rpmFrame.can_id = 0x101;
    rpmFrame.can_dlc = 2;

    rpmFrame.data[0] =
        (vehicle.rpm >> 8) & 0xFF;

    rpmFrame.data[1] =
        vehicle.rpm & 0xFF;

    // -----------------------------
    // CAN Temperature Frame (ID 0x102)
    // -----------------------------
    tempFrame.can_id = 0x102;
    tempFrame.can_dlc = 1;

    tempFrame.data[0] =
        vehicle.engineTemp;

    // -----------------------------
    // Send CAN Frames
    // -----------------------------
    write(can_socket,
          &speedFrame,
          sizeof(speedFrame));

    write(can_socket,
          &rpmFrame,
          sizeof(rpmFrame));

    write(can_socket,
          &tempFrame,
          sizeof(tempFrame));

    vehicle.gps.latitude += 0.0001;
    vehicle.gps.longitude += 0.0001;

       vehicle.gps.latitude += 0.0001;
       vehicle.gps.longitude += 0.0001;

       // MQTT Messages
       char locationMsg[100];
       char statusMsg[100];
       char diagnosticMsg[100];

       snprintf(locationMsg,
                sizeof(locationMsg),
                "Latitude=%.4f Longitude=%.4f",
                vehicle.gps.latitude,
                vehicle.gps.longitude);

       snprintf(statusMsg,
                sizeof(statusMsg),
                "Speed=%d Fuel=%d",
                vehicle.speed,
                vehicle.fuel);

       snprintf(diagnosticMsg,
                sizeof(diagnosticMsg),
                "RPM=%d EngineTemp=%d",
                vehicle.rpm,
                vehicle.engineTemp);

       // Publish Location
       mosquitto_publish(
           mosq,
           NULL,
           "vehicle/location",
           strlen(locationMsg),
           locationMsg,
           0,
           false);

       // Publish Status
       mosquitto_publish(
           mosq,
           NULL,
           "vehicle/status",
           strlen(statusMsg),
           statusMsg,
           0,
           false);

       // Publish Diagnostics
       mosquitto_publish(
           mosq,
           NULL,
           "vehicle/diagnostics",
           strlen(diagnosticMsg),
           diagnosticMsg,
           0,
           false);

       // Console Output
       std::cout << "\n----- Vehicle Data -----\n";

       std::cout << "Latitude     : "
                 << vehicle.gps.latitude << std::endl;

       std::cout << "Longitude    : "
                 << vehicle.gps.longitude << std::endl;

       std::cout << "Speed        : "
                 << vehicle.speed << " km/h" << std::endl;

       std::cout << "RPM          : "
                 << vehicle.rpm << std::endl;

       std::cout << "Fuel         : "
                 << vehicle.fuel << "%" << std::endl;

       std::cout << "Engine Temp  : "
                 << vehicle.engineTemp << " C" << std::endl;

       sleep(1);
   }

   // Cleanup (not reached in current infinite loop)
   mosquitto_disconnect(mosq);
   mosquitto_destroy(mosq);
   mosquitto_lib_cleanup();

   return 0;
}
