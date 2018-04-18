from L3GD20H import L3GD20H
import time
from datetime import datetime

SAMPLING_FREQ = 0.2 #per second
SAMPLING_TIME = -1 #seconds, set to -1 if run infinitely
MATH_NAN = float('nan')
NUM_AXES = 3
OFFSET = [-21, 0, 300]
DELTA_THETA = [0, 0, 0]

gyro = L3GD20H()

class DataPackage(object):
        
    def __init__(self):
        self.rotation = [MATH_NAN, MATH_NAN, MATH_NAN]
        #self.deltaTheta = [0, 0, 0]
        self.time = datetime.now()

    def setRotation(self, rotationTuple):
        for i in range(NUM_AXES):
            self.rotation[i] = rotationTuple[i] - OFFSET[i]
            DELTA_THETA[i] += round(self.rotation[i]/100)
            
    def printData(self):
        print('---------------------------')        
        print(time.strftime('%Y-%m-%d %H:%M:%S', self.time.timetuple()))
        print('Rotation:    ' + str(tuple(self.rotation)))
        print('Delta Theta: ' + str(tuple(DELTA_THETA)))

def getSensorsData():
    package = DataPackage()
    package.setRotation(gyro.read())
    return package

def main():
    timeElapsed = 0 # in milliseconds
    tempTime = 0

    while(timeElapsed < SAMPLING_TIME or SAMPLING_TIME == -1):
        dataPackage = getSensorsData()
        dataPackage.printData()
        time.sleep(SAMPLING_FREQ)
        timeElapsed += SAMPLING_FREQ

main()
