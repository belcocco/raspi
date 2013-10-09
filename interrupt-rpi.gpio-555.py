#!/usr/bin/env python
# -*- coding: latin-1 *-*
# -*- coding: cp1252 -*-
#Raspberry Pi - GPIO interface
#Mentre due led (rosso e verde) lampeggiano ritmicamente (1/2 sec.) in eterno con cicli di 10 volte,
#dopo la pressione di un tasto/pulsane, si deve accendere un terzo 'led di stato' (giallo) per un certo tempo. 
#Questo tempo varia in base al ciclo di 10 volte, cioè se pigio al quarto si deve accendere 6 cicli,
#se pigio al due si deve accendere per 8, se pigio al sette solo per 3,
import RPi.GPIO as GPIO
#from time import sleep 
import time
################################## Inizializzazioni
GPIO.setmode(GPIO.BCM)
ic555In=11			#Out sul pin 3 del 555
ledOut=[7,8,25]			#2 Led per accensione ritmica (GPIO 7=rosso; GPIO 8=verde)
GPIO.setup(ic555In,GPIO.IN)
for a in ledOut:
        GPIO.setup(a,GPIO.OUT)
        GPIO.output(a, False)   #Spegne tutti i led interessati (2 led ritmici e led di stato) 
        time.sleep(0.01)
currentLed=0
contaCicli=0
contaTic=0
ticRising=0
ticFalling=0
pin=ledOut[currentLed]
print time.strftime('%S')	#stampa l'ora di partenza del conteggio
secondi_inizio=time.strftime('%S')	#stampa l'ora di partenza del conteggio

################################### CALLBACK routines
def accendiLedGiallo_CBack (ic555In):
	currentLed=2
#        print "interruptRoutine di CALLBACK: Accendi Led Giallo"
	pin=ledOut[currentLed]
        GPIO.output(pin,True)
#	print "ticRising", ticRising
#	ticRising=ticRising+1
#	print ticRising
#	return ticRising+1
#	GPIO.add_event_detect(ic555In, GPIO.FALLING)	#Evento per intercettare i fronti di discesa (FALLING)
#	GPIO.add_event_callback(ic555In, spegniLedGiallo_CBack, bouncetime=10)

def spegniLedGiallo_CBack (ic555In):
        currentLed=2
#        print "interruptRoutine di CALLBACK: Spegni LED Giallo"
        pin=ledOut[currentLed]
        GPIO.output(pin,False)
#	print "ticFalling", ticFalling
#        ticFalling=ticFalling+1
#	print "ticFalling", ticFalling
#	return ticFalling+1
#	GPIO.add_event_detect(ic555In, GPIO.RISING)	#Evento per intercettare i fronti di salita (RISING) dopo il primo
#	GPIO.add_event_callback(ic555In, accendiLedGiallo_CBack, bouncetime=10)

#Evento per intercettare il 1° fronte di salita (RISING)
GPIO.add_event_detect(ic555In, GPIO.BOTH)	#Evento per intercettare il 1° fronte di salita (RISING)
#GPIO.add_event_detect(ic555In, GPIO.FALLING)	#Evento per intercettare i fronti di discesa (FALLING)
GPIO.add_event_callback(ic555In, accendiLedGiallo_CBack)#, bouncetime=10)
GPIO.add_event_callback(ic555In, spegniLedGiallo_CBack)#, bouncetime=10)

try:
	#TEST dell'input
	#while True:
		#status=GPIO.input(ic555In)
		#if status==1:
		#	print "ALTO",status
		#else:
		#	print "BASSO",status
		#sleep(0.01)

################################### Loop di lavoro
        while True:
#	        print ticRising, ticFalling
		GPIO.output(pin,True)
		pin=ledOut[currentLed+1]
		GPIO.output(pin,False)
		time.sleep(0.25)
		if GPIO.event_detected(ic555In):
			ticRising=ticRising+1
		currentLed=currentLed+1
		pin=ledOut[currentLed]
		
                GPIO.output(pin,True)
                pin=ledOut[currentLed-1]
                GPIO.output(pin,False)
                time.sleep(0.25)
		if GPIO.event_detected(ic555In):
			ticRising=ticRising+1
		currentLed=0
		contaTic=contaTic+1
		if contaTic==60:
#			GPIO.output(25,False)
#			print "60 tic"
			contaCicli=contaCicli+1
			contaTic=0
			print "nr. Cicli ",contaCicli			
		secondi_fine=time.strftime('%S')	#stampa l'ora di partenza del conteggio
		if (secondi_fine-secondi_inizio)>=1:
			break


except KeyboardInterrupt:
        print " "
	print time.strftime('%S')       #stampa l'ora di fine conteggio
	print "Fatti ", ticRising, "tic RISING"	,"***** Fatti ", ticFalling, "tic FALLING"
        print "Ciao !"
        GPIO.cleanup()
	GPIO.setwarnings(False)
#GPIO.cleanup()


