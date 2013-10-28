#!/usr/bin/env python
#Raspberry Pi - GPIO interface
#Relay 

import RPIO
from time import sleep

PINOUT=11
RPIO.setup(PINOUT, RPIO.OUT)


try:
	while 1:
		RPIO.output(PINOUT,True)
		sleep(1)
		RPIO.output(PINOUT,False)
		sleep(0.5)

except KeyboardInterrupt:
        print " "
        print "Ciao !"
        RPIO.cleanup()
RPIO.cleanup()


