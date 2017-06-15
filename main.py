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
SHOW_PREVIEW = True
VIDEO_NAME = 'recording'
VIDEO_INTERVAL = 5 #seconds
RECORD_TIME = 10; #
NUM_IMAGES = 3;

CAMERA_CONNECTED = False #Dont touch this

#Others
SAMPLING_FREQ = 0.1 #per second
SAMPLING_TIME = -1 #seconds, set to -1 if run infinitely
MATH_NAN = float('nan')


#-----------------IMPORTING LIBRARIES-----------------#
from ADXL345 import ADXL345
from MPL3115A2 import MPL3115A2
import MCP9808 as MCP9808
from L3GD20H import L3GD20H
from picamera import PiCamera
from gps3.agps3threaded import AGPS3mechanism

import smbus
import time
import math
#import csv

#--------------------DATA PACKAGE--------------------#

class DataPackage(object):
    
    #The data is formatted in the form (pressure (Pa), temperature (F), attitude(x,y,z))
        
    def __init__(self):
        self.pressure = MATH_NAN
        self.temperature = MATH_NAN
        self.attitude = [MATH_NAN, MATH_NAN, MATH_NAN]
        self.altTemperature = MATH_NAN
        self.rotation = [MATH_NAN, MATH_NAN, MATH_NAN]
        self.coordinates = [MATH_NAN, MATH_NAN]
        self.speed = MATH_NAN
        self.course = MATH_NAN
        self.time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        self.gpstime = MATH_NAN
        self.gpsHeight = MATH_NAN

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

    def setCoordinates(self, coords):
        self.coordinates[0] = coords[0]
        self.coordinates[1] = coords[1]

    def setSpeed(self, speed):
        self.speed = speed

    def setCourse(self, course):
        self.course = course
        
    def setGPSTime(self, gpstime):
        self.gpstime = gpstime

    def setGPSHeight(self, gpsh):
        self.gpsHeight = gpsh

    def getData(self):
        return (self.pressure, self.temperature, tuple(self.attitude), self.altTemperature)

    #For testing only
    def printData(self):
        print('---------------------------')
        print(self.time +'\n')
        print('Height: ' + str(self.pressure) + ' m')
        print('Temperature: ' + str(self.temperature) + ' F')
        print('Acceleration: ' + str(tuple(self.attitude)))
        print('Rotation: ' + str(tuple(self.rotation)))
        print('\nGPS Time: ' + self.gpstime)
        print('Coordinates: ' + str(tuple(self.coordinates)))
        print('GPS Height: ' + str(self.gpsHeight))
        print('Speed: ' + str(self.speed))
        print('Course: ' + str(self.course))
        print('---------------------------')
        #print('%s, %s, %s, %s \n' % (str(tuple(self.attitude)), str(tuple(self.rotation)), self.pressure, self.temperature))

#------------------INITIALIZE SENSORS------------------#

alt = MPL3115A2(Alt_Address)

accel = ADXL345(Accel_Address)

temp = MCP9808.MCP9808(Temp_Address)
temp.begin()

gyro = L3GD20H()

currentTimeStr = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
outputTxtName = currentTimeStr + '-output.txt'

try:
    camera = PiCamera()
    CAMERA_CONNECTED = True
except:
    print('Camera Failed to Connect.')
    pass

while(True):
    try:
        with open(outputTxtName, 'x+') as output:
            output.write(currentTimeStr + '\n')
            break
    except FileExistsError:
        outputTxtName = outputTxtName[:-4] + '(1)' + '.txt'

agps_thread = AGPS3mechanism()  # Instantiate AGPS3 Mechanisms
agps_thread.stream_data()  # From localhost (), or other hosts, by example, (host='gps.ddns.net')
agps_thread.run_thread()  # Throttle time to sleep after an empty lookup, default '()' 0.2 two tenths of a second
    


#-------------------HELPER FUNCTIONS-------------------#

def c_to_f(c):
	return c * 9.0 / 5.0 + 32.0

def outputSensorData(package, textfile):
    
	outputString = ''

	outputString += package.time + ','
    
	for item in package.attitude:
		outputString += str(item) + ','

	for item in package.rotation:
		outputString += str(item) + ','

	outputString += str(package.pressure) + ','
	
	outputString += str(package.temperature) +','

	outputString += str(package.gpstime) + ','

	for item in package.coordinates:
		outputString += str(item) + ','

	outputString += str(package.gpsHeight) + ','	
	outputString += str(package.speed) + ','
	outputString += str(package.course)
	
	textfile.write('%s\n' % (outputString))
	#textfile.write(str(tuple(package.attitude)) + str(tuple(package.rotation)) + str(package.pressure) + str(package.temperature))
        
	
def remainder(a, b):
    c = int(a/b)
    return a - c*b

#----------------------MAIN LOOP----------------------#

def getSensorsData():
    
    package = DataPackage()
    
    altData = alt.read()
    package.setPressure(altData[0])
    package.setAltTemperature(altData[1])
   
    package.setAttitude(accel.read())

    package.setTemperature(temp.read())

    package.setRotation(gyro.read())

    package.gpstime = agps_thread.data_stream.time
    coords = (agps_thread.data_stream.lat, agps_thread.data_stream.lon)
    package.setCoordinates(coords)
    package.setSpeed(agps_thread.data_stream.speed)
    package.setCourse(agps_thread.data_stream.track)
    package.setGPSHeight(agps_thread.data_stream.alt)

    return package

def main():
    
    try:
        if(CAMERA_CONNECTED):
            #camera.start_recording('videos/' + VIDEO_NAME + '0.h264')

            if(SHOW_PREVIEW):
                camera.start_preview(fullscreen = False, window = (100, 20, 640, 480))
    except:
        print('Camera went wrong 0')
        pass

    imgCount = 0
    videoCount = 0
    
    timeElapsed = 0 # in milliseconds

    while(timeElapsed < SAMPLING_TIME or SAMPLING_TIME == -1):
        

        #Get Images
        try:
            if(CAMERA_CONNECTED and NUM_IMAGES > 0 and i % int((RECORD_TIME/NUM_IMAGES)) == 1):
                #camera.capture('images/image' + str(imgCount) + '.jpg', use_video_port=True)
                imgCount += 1
        except:
            pass

        #Get Video
        try:
            if(CAMERA_CONNECTED and remainder(timeElapsed, VIDEO_INTERVAL) == 0):
                videoCount += 1
                #camera.stop_recording()
                #camera.start_recording('videos/' + VIDEO_NAME + str(videoCount) + '.h264')
                print('video ' + str(videoCount))
        except:
            print('Camera went wrong!')
            pass
        
        dataPackage = getSensorsData()
        dataPackage.printData()

        #text_file = open("Output.txt", "a")
        #outputSensorData(dataPackage, text_file)
        #text_file.write('%s, %s, %s, %s \n' % (str(tuple(dataPackage.attitude)), str(tuple(dataPackage.rotation)), dataPackage.pressure, dataPackage.temperature))
        #sorry Edward just delete the next row and get rid of the pound above
        #text_file.write('%s, ' % (str(tuple(dataPackage.attitude))))
        #text_file.write('%s,\n' % (str(tuple(dataPackage.attitude))))
        #text_file.close()

        with open(outputTxtName, 'a') as output:
            outputSensorData(dataPackage, output)
        
        #csvfile = open('Output.csv', 'a')
        #csvwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        #csvwriter.writerows([str(tuple(dataPackage.attitude)), str(tuple(dataPackage.rotation)), str(dataPackage.pressure), str(dataPackage.temperature)])
        #csvfile.close()
        
        time.sleep(SAMPLING_FREQ)
        timeElapsed += SAMPLING_FREQ

    
    
    if(CAMERA_CONNECTED):
        camera.stop_recording()

        if(SHOW_PREVIEW):
            camera.stop_preview()

try:
    main()
except KeyboardInterrupt:
    
    if(CAMERA_CONNECTED):
        camera.stop_recording()

        if(SHOW_PREVIEW):
            camera.stop_preview()
            
    print("\nScript ended by keyboard interrupt")
        
        

        
        
        
    
