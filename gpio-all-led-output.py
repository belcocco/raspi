#!/usr/bin/env python
# -*- coding: latin-1 *-*
# -*- coding: cp1252 -*-

#Raspberry Pi - GPIO interface
#Tutti i 6 led vengono accesi uno dopo l'altro (GPIO 7,8,25,24,23,18 OUTPUTs)
#quando viene premuto il pulsante (GPIO 11 INPUT)
import RPi.GPIO as GPIO
from time import sleep

########################### INIZIALIZZAZIONI
GPIO.setmode(GPIO.BCM)
GPIO.setup(11,GPIO.IN)

pippo=[7,8,25,24,23,18]     # nr. 6 led per l'output
for a in pippo:
	GPIO.setup(a,GPIO.OUT)
	GPIO.output(a, False)   #Spegne i 6 led
	sleep(0.01)

#Aspetta il pulsante GPIO 11 (del circuito 555)
buttonIn=False
while buttonIn==False:
	buttonIn=GPIO.input(11)		#Esce con logica pull-down:  True (chiuso=1)

try:
	while 1:
		for a in pippo:
        		GPIO.output(a, True)   #Accende i 6 led
        		sleep(0.2)
		sleep(0.5)
		for a in pippo:
        		GPIO.output(a, False)   #Spegne i 6 led
        		sleep(0.1)

except KeyboardInterrupt:
        print " "
        print "Ciao !"
        GPIO.setwarnings(False)
        GPIO.cleanup()
GPIO.setwarnings(False)
GPIO.cleanup()



