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
GPIO.setmode(GPIO.BCM)		#Sulla Rivista GPIO.setmode(GPIO,BOARD)
GPIO.setup (11, GPIO.IN)	#Sulla Rivista GPIO.setup (11, GPIO.IN)
GPIO.setup (8, GPIO.OUT)	#Sulla Rivista GPIO.setup (12, GPIO.OUT)
GPIO.setup (10, GPIO.IN)	#Sulla Rivista GPIO.setup (13, GPIO.IN)
GPIO.setup (22, GPIO.OUT)	#Sulla Rivista GPIO.setup (15, GPIO.OUT)



while True:
	if not GPIO.input(11):
		if GPIO.input(10):
			print "The door is open please close the door and try again."
			GPIO.output(22, True)
			sleep(.3)
			GPIO.output(22, False)
			pippo = 3
		while pippo > 0:
			GPIO.output(8, True)
			sleep(.3)
			GPIO.output(8, False)
			sleep(.3)
			pippo -= 1
		else:
			active = True
			activated = False
			sleep(.1)
			if GPIO.input(11):
				print "Alarm Armed"
				while active == True:
					GPIO.output(8,False)
					if not GPIO.input(11):
						sleep(.1)
						if GPIO.input(11):
							print "Alarm Disarmed"
							sleep(.1)
							active = False
					if GPIO.input(10):
						print "**** Alarm !!! ****"
						activated = True
						GPIO.output(22, True)
						sleep(10)
						GPIO.output(22, False)
						while activated == True:
							if not GPIO.input(11):
								sleep(.1)
								if GPIO.input(11):
									print "Alarm Disarmed"
									sleep(.1)
									active = False
									activated = False
							else:
								GPIO.output(8, True)
								sleep(.3)
								GPIO.output(8, False)
								sleep(.3)
	else:
		GPIO.output(8,True)
