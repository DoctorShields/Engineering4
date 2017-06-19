#python3

class MPL3115A2(object):

    def __init__(self, address = 0x60):
        import smbus      
        self.bus = smbus.SMBus(1)
        self.Altimeter_Address = address
        self.TEMP_MSB = 0x04
        self.TEMP_LSB = 0x05

        self.CTRL_REG_1 = 0x26
        self.DATA_CONFIG_REG = 0x13

        import Adafruit_GPIO.I2C as I2C
        i2c = I2C
        self._device = i2c.get_i2c_device(address)

        try:
            #Altimeter mode
            self.bus.write_byte_data(self.Altimeter_Address, self.CTRL_REG_1, 0xB9)
            #Data Ready event
            self.bus.write_byte_data(self.Altimeter_Address, self.DATA_CONFIG_REG, 0x07)
        except:
            print('Unable to initialize ALT')
            pass

    def read(self, celsius = False):
        # import time
        # Set to active mode, altimeter mode
        # (0xB9 (185) Active Mode, OSR = 128, Altimeter mode)
        #self.bus.write_byte_data(self.Altimeter_Address, self.CTRL_REG_1, 0xB9)

        # (0x07 Data Ready event enabled for altitude, pressure and temperature)
        #self.bus.write_byte_data(self.Altimeter_Address, self.DATA_CONFIG_REG, 0x07)

        # (0xB9 (185) Active Mode, OSR = 128, Altimeter mode)
        #self.bus.write_byte_data(self.Altimeter_Address, self.CTRL_REG_1, 0xB9)
        #time.sleep(1) #??

        # (0x39 (57) Active Mode, OSR = 128, Barometer Mode)
        #self.bus.write_byte_data(self.Altimeter_Address, self.CTRL_REG_1, 0x39)
        rdata = (float('nan'), float('nan'));

        try:
            # Read data from 0x00(00), 6 bytes
            # [status, tHeightMSB1, tHeight MSB, tHeight LSB, temp MSB, temp LSB]
            data = self.bus.read_i2c_block_data(self.Altimeter_Address, 0x00, 6)

            # Convert data to 20 bits (?)
            tHeight = ((data[1] * 65536) + (data[2] * 256) + (data[3]&0xF0))/16
            altitude = (tHeight/16.0)

            temp = ((data[4] * 256) + (data[5] & 0xF0)) /16 
            cTemp = temp / 16
            fTemp = cTemp * 1.8 + 32

            if(celsius):
                rdata = (altitude, cTemp)
            else:
                rdata = (altitude, fTemp)
        
        except:
            #print('Unable to get ALT data')
            pass

        finally:
            return rdata

        



