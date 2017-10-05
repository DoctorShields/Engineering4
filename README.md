# SENTINEL-1 Sensors Drivers

Drivers for altimeter MPL3115A5, accelerometer ADXL345, magnetometer MCP9808 and gyroscope L3GD20H.

## Setup Instructions:
1. Install bcm2835 library
2. Install gps3
3. Enable I2C, SPI, disable serial shell, enable serial interface
4. In shell: 
```
  $ sudo apt-get install gpsd gpsd-clients python-gps  
  $ sudo systemctl stop gpsd.socket
  $ sudo systemctl disable gpsd.socket
  $ sudo gpsd /dev/ttyAMA0 -F /var/run/gpsd.sock
```  
5. install adafruit gpio library (for python 3!!)
6. Enable camera
