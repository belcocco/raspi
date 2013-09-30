#!/usr/bin/env python
# -*- coding: latin-1 *-*
# -*- coding: cp1252 -*-
#Raspberry Pi - GPIO interface
#Prova test PWM 
import RPi.GPIO as GPIO
from time import sleep
################################### Inizializzazioni
PWM_CHANNEL=18
GPIO.setmode(GPIO.BCM)
GPIO.setup(PWM_CHANNEL, GPIO.OUT)

pwm = GPIO.PWM(PWM_CHANNEL, 50)  # channel=18 (pin=12) frequency=50Hz
pwm.start(0)
try:
    print "Per fermare <Ctrl-C>"
    while 1:
        for dc in range(0, 101, 5):
            pwm.ChangeDutyCycle(dc)
            sleep(0.1)
        for dc in range(100, -1, -5):
            pwm.ChangeDutyCycle(dc)
            sleep(0.1)
except KeyboardInterrupt:
    pass
    print "STOP!"
    print "Ciao!"
    pwm.stop()
GPIO.cleanup()




