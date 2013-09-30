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
GPIO.setmode(GPIO.BCM)
buttonIn=False
luceIn=False
ledOnfotores=False
ledOn555=False
ic555In=11
fotoresIn=17
ledPins555=[7,8,25]	# nr. 3 led per input da 555
ledPinsfotores=[24,23,18]  #gli altri 3 Led per accensione con buio
GPIO.setup(fotoresIn,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
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
try:
	while 1:
		#Guarda se BUIO o LUCE
		if GPIO.input(fotoresIn):  #Esce con logica pull-up True ovvero con pulsante chiuso=input 0=True
			print "1_____>LUCE"          
    	        	sleep(1)
		else:	
			print "2_____>BUIO"          
               		#Accendi tutti i led
                	for a in ledPinsfotores:
       	                	GPIO.output(a, True)
               	        	sleep(0.1)
	        	#Spegne tutti i led
                	for a in ledPinsfotores:
                        	GPIO.output(a, False)
                        	sleep(0.1)
                        	ledOnfotores=False


except KeyboardInterrupt:
	print " "
	print "Ciao !"
	GPIO.cleanup()
#GPIO.cleanup()







