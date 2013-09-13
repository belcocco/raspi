#!/usr/bin/env python
#Lettura ingresso GPIO-22 alla pressione del pulsante
#Logica con resistore di pull-up: chiuso=0-LOW ;aperto=1-HIGH

import RPi.GPIO as GPIO
from time import sleep
#Inizializzazioni
GPIO.cleanup()
GPIO.setmode(GPIO.BCM)
ledPins=[9,10,11]  #Led rosso, verde, giallo
buttonPin=8
for a in ledPins:
	GPIO.setup(a,GPIO.OUT)
	GPIO.output(a, False)
GPIO.setup(buttonPin, GPIO.IN)
currentLed=0
pin=ledPins[currentLed]
buttonIn=GPIO.input(buttonPin)
GPIO.output(pin, True)

print "Stato del pulsante NON premuto ", "---> ", buttonIn, "Con resistenza di pull-up"
print "Per accendere il LED successivo",currentLed+1, "premi il pulsante"

while 1:
	buttonIn=GPIO.input(buttonPin)
	if buttonIn == False:		#In questo caso pull-down deve essere False (chiuso=0)
		GPIO.output(pin, True)
		if currentLed==2:
			currentLed=0
		else:
			currentLed = currentLed+1
		old_pin=ledPins[currentLed-1]
		GPIO.output(old_pin, False)
		pin=ledPins[currentLed]
		GPIO.output(pin, True)
		print "Premi ancora il pulsante per accendere il prossimo LED ", currentLed
		sleep(0.5)


