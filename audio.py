import os
from datetime import datetime
from time import sleep

startingTime = datetime.now()
currentTimeStr = startingTime.strftime('%Y-%m-%d-%H:%M:%S')

while True:
    try:
        dir = os.path.dirname(__file__)
        start_audio_command = "arecord --device=hw:1,0 --format S16_LE --rate 44100 -V mono -c1 "
        start_audio_command += dir + "/audio/" + currentTimeStr + ".wav"
        os.system(start_audio_command)
    except:
        sleep(1)
        continue

    break
