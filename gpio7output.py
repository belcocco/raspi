#!/usr/bin/env python

import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)

GPIO.setmode(GPIO.BCM)
GPIO.setup(7,GPIO.OUT)

while 1:
	GPIO.output(7,True)
	time.sleep(0.1)
	GPIO.output(7,False)
	time.sleep(0.1)

