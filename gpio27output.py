#!/usr/bin/env python
#Raspberry Pi - GPIO interface
#Led flashing 1 sec
import RPi.GPIO as GPIO
from time import sleep

GPIO.cleanup()
GPIO_channel=27
GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_channel,GPIO.OUT)

while 1:
	GPIO.output(GPIO_channel,True)
	sleep(1)
	GPIO.output(GPIO_channel,False)
	sleep(1)

