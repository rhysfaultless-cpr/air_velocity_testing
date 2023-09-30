# air_velocity_testing

## Installation Notes

1.  Set up a mini-ITX computer with Ubuntu 22.04
2.  Adding serial device permissions
    -   Serial device found: `Bus 001 Device 006: ID 1a86:7523 QinHeng Electronics CH340 serial converter`
    -   Added permissions for the serial port: `sudo chown administrator /dev/ttyUSB0`
3.  Install Python tools and libraries
    -   `sudo apt install python3-pip`
    -   `python3 -m pip install pyserial`
    -   `pip3 install mysql-connector-python`
