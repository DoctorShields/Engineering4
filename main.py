#-----------------MANIFEST CONSTANTS-----------------#
#ALT
Alt_Address = 0x60

#ACCEL
Accel_Address = 0x1d
NUM_AXES = 3

#TEMP
Temp_Address = 0x19
USE_CELSIUS = False

#PiCamera
SHOW_PREVIEW = False
VIDEO_NAME = 'recording.h264'
RECORD_TIME = 10;
NUM_IMAGES = 3;

CAMERA_CONNECTED = False #Dont touch this

#Others
SAMPLING_FREQ = 0.1 #per second


#-----------------IMPORTING LIBRARIES-----------------#
from ADXL345 import ADXL345
from MPL3115A2 import MPL3115A2
import MCP9808 as MCP9808
from L3GD20H import L3GD20H
from picamera import PiCamera

import smbus
import time

#--------------------DATA PACKAGE--------------------#

class DataPackage(object):
    
    #The data is formatted in the form (pressure (Pa), temperature (F), attitude(x,y,z))
        
    def __init__(self):
        self.pressure = 0
        self.temperature = 0
        self.attitude = [0,0,0]
        self.altTemperature = 0
        self.rotation = [0,0,0]

    def setPressure(self, pressure):
        self.pressure = pressure

    def setTemperature(self, temperature):
        self.temperature = temperature

    def setAltTemperature(self, temperature):
        self.altTemperature = temperature

    def setAttitude(self, attitudeTuple):
        for i in range(NUM_AXES):
            self.attitude[i] = attitudeTuple[i]

    def setRotation(self, rotationTuple):
        for i in range(NUM_AXES):
            self.rotation[i] = rotationTuple[i]

    def getData(self):
        return (self.pressure, self.temperature, tuple(self.attitude), self.altTemperature)

    #For testing only
    def printData(self):
        print('Pressure: ' + str(self.pressure) + ', Temperature: ' + str(self.temperature) + ', Acceleration: ' + str(tuple(self.attitude)) + ', Rotation: ' + str(tuple(self.rotation)))

#------------------INITIALIZE SENSORS------------------#

alt = MPL3115A2(Alt_Address)

accel = ADXL345(Accel_Address)

temp = MCP9808.MCP9808(Temp_Address)
temp.begin()

gyro = L3GD20H()

try:
    camera = PiCamera()
    CAMERA_CONNECTED = True
except:
    print('Camera Failed to Connect.')
    pass




#-------------------HELPER FUNCTIONS-------------------#

def c_to_f(c):
	return c * 9.0 / 5.0 + 32.0

def outputSensorData(package, textfile):
	textfile.write('{%s, %s}, %s, %s \n' % (str(tuple(package.attitude)), str(tuple(package.rotation)), package.pressure, package.temperature))
	
	return 0

#----------------------MAIN LOOP----------------------#

def getSensorsData():
    
    package = DataPackage()

    
    altData = alt.read()
    package.setPressure(altData[0])
    package.setAltTemperature(altData[1])
   
    package.setAttitude(accel.read())

    package.setTemperature(temp.read())

    package.setRotation(gyro.read())

    return package

def main():
    
    try:
        if(CAMERA_CONNECTED):
            camera.start_recording(VIDEO_NAME)

            if(SHOW_PREVIEW):
                camera.start_preview()
    except:
        pass

    imgCount = 0
    
    #DELETE THIS LATER
    for i in range(int(RECORD_TIME * 1/SAMPLING_FREQ)):

        try:
            if(CAMERA_CONNECTED and NUM_IMAGES > 0 and i % int((RECORD_TIME/NUM_IMAGES)) == 1):
                camera.capture('images/image' + str(imgCount) + '.jpg', use_video_port=True)
                imgCount += 1
        except:
            pass
        text_file = open("Output.txt", "a")
        dataPackage = getSensorsData()
        dataPackage.printData()
        #outputSensorData(dataPackage, text_file)
        text_file.write('{%s, %s}, %s, %s \n' % (str(tuple(dataPackage.attitude)), str(tuple(dataPackage.rotation)), dataPackage.pressure, dataPackage.temperature))
        text_file.close()
        
        
        
        time.sleep(SAMPLING_FREQ)

    
    
    if(CAMERA_CONNECTED):
        camera.stop_recording()

        if(SHOW_PREVIEW):
            camera.stop_preview()

main()
#text_file.close()
        
        

        
        
        
    
