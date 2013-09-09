#!/usr/bin/env python

#Raspberry-py
#Esempio per gestire input e output (GPIO)
import RPi.GPIO as GPIO, feedparser
from time import sleep

GPIO.cleanup()
GPIO.setmode(GPIO.BCM)

GPIO.setup(22,GPIO.IN)
GPIO.setup(8,GPIO.OUT)
input_value=0
print input_value
while 1:
	if input_value == 0: 
		input_value=GPIO.input(22)
	print input_value
	input_value=0
	sleep(0.5)


