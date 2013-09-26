#!/usr/bin/env python
# -*- coding: latin-1 *-*
# -*- coding: cp1252 -*-
#Raspberry Pi - GPIO interface
#Tutti gli 11 led vengono accesi uno dopo l'altro
#Con il buio la logica pull-up del fotoresistore accende i led
#ovvero parte la luminaria. Viceversa con la luce tutti i led si spengono.
import RPi.GPIO as GPIO
from time import sleep
################################### Inizializzazioni
GPIO.cleanup()
GPIO.setmode(GPIO.BCM)
ledOn=False
fotoresIn=17
ledPins=[7,8,25,24,23,18]  #6 Led con relativo numero GPIO
GPIO.setup(fotoresIn,GPIO.IN)

while True:
        luceIn=GPIO.input(fotoresIn)  #Esce con logica pull-up True ovvero con pulsante chiuso=input 0=True
	for a in ledPins:
		GPIO.setup(a,GPIO.OUT)
		GPIO.output(a, False)	#Spegne tutti i led
		sleep(0.1)
	for a in ledPins:
#        GPIO.setup(a,GPIO.OUT)
        	GPIO.output(a, True)   #Spegne tutti i led
		sleep(0.1)

################################### Loop di lavoro
#while 1:
#	#Guarda se BUIO o LUCE
#	while ledOn==False:
#       	        luceIn=GPIO.input(fotoresIn)  #Esce con logica pull-up True ovvero con pulsante chiuso=input 0=True
#                                                #con fotoresistenza Luce presente=input 0=True
#    	        sleep(0.01)
#
#		if luceIn==True:
#               #Accendi tutti i led
#	                for a in ledPins:
#        	                GPIO.output(a, True)
#                	        sleep(0.3)
	        #Spegne tutti i led
#	for a in ledPins:
#		GPIO.output(a, False)
#		sleep(0.01)
#		ledOn=False
#	elif ledOn==True:
#		#Accendi tutti i led
#		for a in ledPins:
#			GPIO.output(a, True)
#			sleep(0.01)	
#			ledOn=False
#			buttonIn=False
        #Spegne tutti i led
#        while ledOn==False:
#                for a in ledPins:
#                        GPIO.output(a, False)
#                        sleep(0.1)
#                        ledOn=True

