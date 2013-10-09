#!/usr/bin/env python
#Raspberry Pi - GPIO interface
#Led flashing 1 sec
import RPi.GPIO as GPIO
from time import sleep

GPIO.cleanup()

GPIO.setmode(GPIO.BCM)
GPIO.setup(4,GPIO.OUT)

while 1:
	GPIO.output(4,True)
	sleep(0.5)
	GPIO.output(4,False)
	sleep(3)

