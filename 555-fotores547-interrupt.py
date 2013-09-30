#!/usr/bin/env python
# -*- coding: latin-1 *-*
# -*- coding: cp1252 -*-
#Raspberry Pi - GPIO interface
#Tutti i 6 led colegati sui GPIO OUT vengono accesi secondo lo stato di nr. 2 ingressi
#1)Caso della fotoresistenza:
#  Con la luce vengono accesi i led + cicalino
#  ovvero parte la luminaria. Viceversa con il i led si spengono e il cicalino tace
#2)Caso del timer 555:
#  i led si accendono in sincronia con la tempistica impostata dal 555
import RPi.GPIO as GPIO
from time import sleep
################################### Inizializzazioni
GPIO.setmode(GPIO.BCM)
#buttonIn=False
#luceIn=False
#ledOnfotores=False
#ledOn555=False
ic555In=11
fotoresIn=17
ledPins555=[7,8,25]	# nr. 3 led per input da 555
ledPinsfotores=[24,23,18]  #gli altri 3 Led per accensione con buio
GPIO.setup(fotoresIn,GPIO.IN)#,pull_up_down=GPIO.PUD_UP)	#inizializzazione con logica pull-up
GPIO.setup(ic555In,GPIO.IN)#,pull_up_down=GPIO.PUD_IP)	#inizializzazione con logica pull-up
for a in ledPinsfotores:
        GPIO.setup(a,GPIO.OUT)
        GPIO.output(a, False)   #Spegne i 3 led della fotoresistenza
        sleep(0.01)
for a in ledPins555:
	GPIO.setup(a,GPIO.OUT)
	GPIO.output(a, False)	#Spegne i 3 led del 555
	sleep(0.01)

def fotores_CB(fotoresIn):
	print "1----fotores CALLBACK"
	print "2----fotores CALLBACK"
	print "3----fotores CALLBACK"
	a=0
	b=0
	for a in ledPinsfotores:
       		GPIO.output(a, True)
               	sleep(0.1)
	for b in ledPinsfotores:
       		GPIO.output(a, False)
               	sleep(0.1)

def ic555_CB(ic555In):
	print "ic555 CALLBACK"
	a=0
	b=0
	for a in ledPins555:
       		GPIO.output(a, True)
               	sleep(0.01)
	for b in ledPins555:
       		GPIO.output(a, False)
               	sleep(0.1)

################################### Loop di lavoro
try:
	# add falling edge detection on a channel HIGH ----> LOW
	GPIO.add_event_detect(fotoresIn, GPIO.FALLING)#, callback=fotores_CB, bouncetime=1500)
	GPIO.add_event_callback(fotoresIn, fotores_CB, bouncetime=500)
	# add rising edge detection on a channel LOW ----> HIGH
	GPIO.add_event_detect(ic555In, GPIO.RISING)#, callback=ic555_CB, bouncetime=1500) 
	GPIO.add_event_callback(ic555In, ic555_CB, bouncetime=500)
	sleep(1)
	while 1:
		GPIO.event_detected(fotoresIn)
		sleep(1)

		GPIO.event_detected(ic555In)
		sleep(1)

except KeyboardInterrupt:
	print " "
	print "Ciao !"
	GPIO.setwarnings(False)
	GPIO.cleanup()
GPIO.setwarnings(False)
GPIO.cleanup()







