#!/usr/bin/env python

#Raspberry-py
#Esempio per gestire input e output (GPIO)
import RPi.GPIO as GPIO, feedparser
from time import sleep

GPIO.cleanup()
GPIO.setmode(GPIO.BCM)

#GPIO.setup(7,GPIO.IN)
GPIO.setup(2,GPIO.OUT)
GPIO.setup(3,GPIO.OUT)
GPIO.setup(4,GPIO.OUT)
#input_value=0
#print input_value
while 1:
#	if input_value == 0: 
#		input_value=GPIO.input(7)
#	print input_value
#	input_value=0
	GPIO.output(2,False)
	GPIO.output(3,False)
        GPIO.output(4,False)
        sleep(0.3)
        GPIO.output(2,True)
        GPIO.output(3,True)
        GPIO.output(4,True)
        sleep(0.3)


