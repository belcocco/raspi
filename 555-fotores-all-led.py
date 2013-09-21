#!/usr/bin/env python
# -*- coding: latin-1 *-*
# -*- coding: cp1252 -*-
#Raspberry Pi - GPIO interface
#Tutti i 6 led colegati sui GPIO OUT vengono accesi secondo lo stato di nr. 2 ingressi
#1)Caso della fotoresistenza:
#  Con il buio la logica pull-up del fotoresistore accende i led
#  ovvero parte la luminaria. Viceversa con la luce tutti i led si spengono.
#2)Caso del timer 555:
#  i led si accendono in sincronia con la tempistica impostata dal 555
import RPi.GPIO as GPIO
from time import sleep
################################### Inizializzazioni
GPIO.cleanup()
GPIO.setmode(GPIO.BCM)
buttonIn=False
luceIn=False
ledOnfotores=False
ledOn555=False
ic555In=11
fotoresIn=17
ledPins555=[7,8,25]	# nr. 3 led per input da 555
ledPinsfotores=[24,23,18]  #gli altri 3 Led per accensione con buio
GPIO.setup(fotoresIn,GPIO.IN)
GPIO.setup(ic555In,GPIO.IN)
for a in ledPins555:
	GPIO.setup(a,GPIO.OUT)
	GPIO.output(a, False)	#Spegne i 3 led del 555
	sleep(0.1)
for a in ledPinsfotores:
	GPIO.setup(a,GPIO.OUT)
	GPIO.output(a, False)	#Spegne i 3 led della fotoresistenza
	sleep(0.1)

################################### Loop di lavoro
while 1:
	#Guarda se BUIO o LUCE
	#while
	if ledOnfotores==False and luceIn==False:
       	        luceIn=GPIO.input(fotoresIn)  #Esce con logica pull-up True ovvero con pulsante chiuso=input 0=True
                                                #con fotoresistenza Luce presente=input 0=True
#    	        sleep(0.01)
	        if luceIn==True:
			ledOnfotores=True
			print "Accendi i LED----> luceIn=",luceIn
		if ledOnfotores==True and luceIn==True:
               #Accendi tutti i led
	                for a in ledPinsfotores:
        	                GPIO.output(a, True)
                	        sleep(0.01)
                        	ledOnfotores=False
				luceIn=False
	        #Spegne tutti i led
                for a in ledPinsfotores:
                        GPIO.output(a, False)
                        sleep(0.01)
                        ledOnfotores=False

        #Guarda input da 555
        #while
	if ledOn555==False and buttonIn==False:
                buttonIn=GPIO.input(ic555In)  #Esce con logica pull-up True ovvero con pulsante chiuso=input 0=True
                                                #con bottone pigiato=input 0=True
#               sleep(0.01)
                if buttonIn==True:
                        ledOn555=True
                        print "Accendi i LED----> buttonIn=",buttonIn
                if ledOn555==True and buttonIn==True:
               #Accendi tutti i led
                        for a in ledPins555:
                                GPIO.output(a, True)
				sleep(0.01)
                                ledOn555=False
                                buttonIn=False
                #Spegne tutti i led
                for a in ledPins555:
                        GPIO.output(a, False)
                        sleep(0.01)
                        ledOn555=False








