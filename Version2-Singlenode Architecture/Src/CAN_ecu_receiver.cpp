#include <iostream>
#include <cstring>

#include <unistd.h>

#include <linux/can.h>
#include <linux/can/raw.h>

#include <sys/socket.h>
#include <sys/ioctl.h>

#include <net/if.h>

int main()
{
    int can_socket;

    struct sockaddr_can addr;
    struct ifreq ifr;

    struct can_frame frame;

    // Create CAN socket
    can_socket = socket(PF_CAN,
                        SOCK_RAW,
                        CAN_RAW);

    if(can_socket < 0)
    {
        perror("CAN Socket");
        return 1;
    }

    strcpy(ifr.ifr_name, "vcan0");

    if(ioctl(can_socket,
             SIOCGIFINDEX,
             &ifr) < 0)
    {
        perror("ioctl");
        close(can_socket);
        return 1;
    }

    addr.can_family = AF_CAN;
    addr.can_ifindex = ifr.ifr_ifindex;

    if(bind(can_socket,
            (struct sockaddr *)&addr,
            sizeof(addr)) < 0)
    {
        perror("bind");
        close(can_socket);
        return 1;
    }

    std::cout << "ECU Receiver Listening on vcan0...\n";

    while(true)
    {
        int nbytes =
            read(can_socket,
                 &frame,
                 sizeof(frame));

        if(nbytes < 0)
        {
            perror("CAN Read");
            continue;
        }

        switch(frame.can_id)
        {
            case 0x100:
            {
                int speed =
                    frame.data[0];

                std::cout
                    << "Received Speed       : "
                    << speed
                    << " km/h"
                    << std::endl;

                break;
            }

            case 0x101:
            {
                int rpm =
                    (frame.data[0] << 8) |
                     frame.data[1];

                std::cout
                    << "Received RPM         : "
                    << rpm
                    << std::endl;

                break;
            }

            case 0x102:
            {
                int temp =
                    frame.data[0];

                std::cout
                    << "Received Temperature : "
                    << temp
                    << " C"
                    << std::endl;

                break;
            }

            default:
            {
                std::cout
                    << "Unknown CAN ID: 0x"
                    << std::hex
                    << frame.can_id
                    << std::dec
                    << std::endl;

                break;
            }
        }
    }

    close(can_socket);

    return 0;
}
