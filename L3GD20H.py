DEFAULT_ADDRESS = 0x6a #Device I2C slave address

LGD_CTRL_1 = 0x20 #turns on gyro

#Registers holding gyroscope readings
LGD_GYRO_X_LSB = 0x28
LGD_GYRO_X_MSB = 0x29
LGD_GYRO_Y_LSB = 0x2A
LGD_GYRO_Y_MSB = 0x2B
LGD_GYRO_Z_LSB = 0x2C
LGD_GYRO_Z_MSB = 0x2D

def twos_comp_combine(msb, lsb):
    twos_comp = 256*msb + lsb
    if twos_comp >= 32768:
        return twos_comp - 65536
    else:
        return twos_comp

class L3GD20H(object):

    def __init__(self, address=DEFAULT_ADDRESS):
        
        import smbus
        self.bus = smbus.SMBus(1)

        import Adafruit_GPIO.I2C as I2C
        i2c = I2C

        self.address = address

        try:
            self.bus.write_byte_data(address, LGD_CTRL_1, 0x0F) #turn on gyro and set to normal mode
        except:
            pass

    def read(self):
        try:
            gyrox = twos_comp_combine(self.bus.read_byte_data(self.address, LGD_GYRO_X_MSB), self.bus.read_byte_data(self.address, LGD_GYRO_X_LSB))
            gyroy = twos_comp_combine(self.bus.read_byte_data(self.address, LGD_GYRO_Y_MSB), self.bus.read_byte_data(self.address, LGD_GYRO_Y_LSB))
            gyroz = twos_comp_combine(self.bus.read_byte_data(self.address, LGD_GYRO_Z_MSB), self.bus.read_byte_data(self.address, LGD_GYRO_Z_LSB))
            return (gyrox, gyroy, gyroz)
        except:
            return (0,0,0)

        
        
        
