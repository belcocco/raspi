#!/usr/bin/env python
#Raspberry Pi - GPIO interface
#Led flashing 1 sec
import RPi.GPIO as GPIO
from time import sleep

GPIO.cleanup()

GPIO.setmode(GPIO.BCM)
GPIO.setup(8,GPIO.OUT)

while 1:
	GPIO.output(8,True)
	sleep(1)
	GPIO.output(8,False)
	sleep(1)

