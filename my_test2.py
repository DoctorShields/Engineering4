from L3GD20H import L3GD20H
import time

NUM_AXES = 3
OFFSET = [-21, 0, 300]
DELTA_THETA = [0, 0, 0]

gyro = L3GD20H()

class DataPackage(object):
        
    def __init__(self):
        self.rotation = [0,0,0]

    def setRotation(self, rotationTuple):
        for i in range(NUM_AXES):
            self.rotation[i] = rotationTuple[i] - OFFSET[i]
            DELTA_THETA[i] += round(self.rotation[i]/100)
            
    def printData(self):
        print('---------------------------')        
        print('Rotation:    ' + str(tuple(self.rotation)))
        print('Delta Theta: ' + str(tuple(DELTA_THETA)))

def getSensorsData():
    package = DataPackage()
    package.setRotation(gyro.read())
    return package

while True:
    dataPackage = getSensorsData()
    dataPackage.printData()
    time.sleep(.2)

