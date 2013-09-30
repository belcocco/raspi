#!/usr/bin/env python
# -*- coding: latin-1 *-*
# -*- coding: cp1252 -*-
#Raspberry Pi - GPIO interface
#Prova test PWM 
import RPi.GPIO as GPIO
from time import sleep
################################### Inizializzazioni
#GPIO.setmode(GPIO.BOARD)
#GPIO.setup(12, GPIO.OUT)

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)

p = GPIO.PWM(18, 3) 
p.start(50)	#in origine era: p.start(1)
raw_input('Press return to stop:')   # use raw_input for Python 2
p.stop()
GPIO.cleanup()



