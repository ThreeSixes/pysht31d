#!/usr/bin/python

import sht31d
import time

thS = sht31d.sht31d()
thS.sendCmd16(thS.cmdCntHiRep4Hz, wait = True)

while True:
    thS.readSensor()
    print("Temperature: %s C" %thS.temperature)
    print("Humidity   : %s RH" %thS.humidity)
    time.sleep(1)


