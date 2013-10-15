#!/usr/bin/env python
#Raspberry Pi - GPIO interface
#Led flashing 1 sec
import RPi.GPIO as GPIO
from time import sleep

GPIO.cleanup()

GPIO.setmode(GPIO.BCM)
GPIO.setup(11,GPIO.OUT)
GPIO.setup(23,GPIO.OUT)

try:
	while 1:
		GPIO.output(11,True)
		GPIO.output(23,True)
		sleep(0.5)
		GPIO.output(11,False)
		GPIO.output(23,False)
		sleep(0.3)

except KeyboardInterrupt:
        print " "
        print "Ciao !"
        GPIO.setwarnings(False)
        GPIO.cleanup()
GPIO.setwarnings(False)
GPIO.cleanup()


