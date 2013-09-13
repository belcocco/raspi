#!/usr/bin/env python
#Raspberry Pi - GPIO interface
#Tutti i 12 led vengono accesi uno dopo l'altro
#quando viene premuto il pulsante rosso
import RPi.GPIO as GPIO
from time import sleep

GPIO.cleanup()

GPIO.setmode(GPIO.BCM)
GPIO.setup(7,GPIO.IN)
GPIO.setup(8,GPIO.OUT)
GPIO.setup(9,GPIO.OUT)
GPIO.setup(10,GPIO.OUT)
GPIO.setup(11,GPIO.OUT)
GPIO.setup(17,GPIO.OUT)
GPIO.setup(18,GPIO.OUT)
GPIO.setup(22,GPIO.OUT)
GPIO.setup(23,GPIO.OUT)
GPIO.setup(24,GPIO.OUT)
GPIO.setup(25,GPIO.OUT)
GPIO.setup(27,GPIO.OUT)

buttonIn=False
while buttonIn==False:
	buttonIn=GPIO.input(7)		#Esce con logica pull-down:  True (chiuso=1)
	sleep(0.1)
#	GPIO.setup(7,GPIO.OUT)		#GPIO 7 da input passa ad output
#GPIO.output(25,True)
#sleep(0.5)

while 1:
	#Accendi tutti i led
#	GPIO.output(7,True)
#	sleep(0.2)
        GPIO.output(8,True)
        sleep(0.1)
        GPIO.output(25,True)
        sleep(0.1)
        GPIO.output(24,True)
        sleep(0.1)
        GPIO.output(23,True)
        sleep(0.1)
        GPIO.output(18,True)
        sleep(0.1)
        GPIO.output(11,True)
        sleep(0.1)
        GPIO.output(9,True)
        sleep(0.1)
        GPIO.output(10,True)
        sleep(0.1)
        GPIO.output(22,True)
        sleep(0.1)
        GPIO.output(27,True)
        sleep(0.1)
        GPIO.output(17,True)
        sleep(0.1)

	#Spegni tutti i led
#        GPIO.output(7,False)
#        sleep(0.2)
        GPIO.output(8,False)
        sleep(0.02)
        GPIO.output(25,False)
        sleep(0.02)
        GPIO.output(24,False)
        sleep(0.02)
        GPIO.output(23,False)
        sleep(0.02)
        GPIO.output(18,False)
        sleep(0.02)
        GPIO.output(11,False)
        sleep(0.02)
        GPIO.output(9,False)
        sleep(0.02)
        GPIO.output(10,False)
        sleep(0.02)
        GPIO.output(22,False)
        sleep(0.02)
        GPIO.output(27,False)
        sleep(0.02)
        GPIO.output(17,False)
        sleep(1)



