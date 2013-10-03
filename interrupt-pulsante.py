#!/usr/bin/env python
# -*- coding: latin-1 *-*
# -*- coding: cp1252 -*-
#Raspberry Pi - GPIO interface
#Mentre due led (rosso e verde) lampeggiano ritmicamente (1/2 sec.) in eterno con cicli di 10 volte,
#dopo la pressione di un tasto/pulsane, si deve accendere un terzo led (giallo) per un certo tempo. 
#Questo tempo varia in base al ciclo di 10 volte, cioè se pigio al quarto si deve accendere 6 cicli,
#se pigio al due si deve accendere per 8, de pigio al sette solo per 3,
import RPi.GPIO as GPIO
from time import sleep
################################## Inizializzazioni
GPIO.setmode(GPIO.BCM)
pulsanteIn=9
ledOut=[7,8,25]  			#2 Led per accensione ritmica (GPIO 7=rosso; GPIO 8=verde)
GPIO.setup(pulsanteIn,GPIO.IN)
for a in ledOut:
        GPIO.setup(a,GPIO.OUT)
        GPIO.output(a, False)   #Spegne tutti i led interessati (2 led ritmici e led di stato) 
        sleep(0.01)
currentLed=0
contaCicli=0
pin=ledOut[currentLed]

################################### CALLBACK routines
def accendiLedGiallo_CBack (pulsanteIn):
	currentLed=2
        print "interruptRoutine di CALLBACK per pulsante premuto"
	pin=ledOut[currentLed]
        GPIO.output(pin,True)

################################### Loop di lavoro
try:
        # add rising edge detection on a channel LOW ----> HIGH
        GPIO.add_event_detect(pulsanteIn, GPIO.RISING)		#, callback=ic555_CB, bouncetime=1500) 
        GPIO.add_event_callback(pulsanteIn, accendiLedGiallo_CBack, bouncetime=500)
        while True:
		GPIO.output(pin,True)
		pin=ledOut[currentLed+1]
		GPIO.output(pin,False)
		sleep(0.25)
                GPIO.event_detected(pulsanteIn)

		currentLed=currentLed+1
		pin=ledOut[currentLed]
		
                GPIO.output(pin,True)
                pin=ledOut[currentLed-1]
                GPIO.output(pin,False)
                sleep(0.25)
                GPIO.event_detected(pulsanteIn)
		currentLed=0
		contaCicli=contaCicli+1
		if contaCicli==20:
			GPIO.output(25,False)
			print "Spento 25"
			contaCicli=0
		else:
			print "Tic ",contaCicli			
except KeyboardInterrupt:
        print " "
        print "Ciao !"
        GPIO.cleanup()
	GPIO.setwarnings(False)
#GPIO.cleanup()

