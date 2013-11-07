#!/usr/bin/env python
# -*- coding: latin-1 *-*
# -*- coding: cp1252 -*-
#Raspberry Pi - GPIO interface
#Prova test PWM 
import RPIO 
from RPIO import PWM
from time import sleep
################################### Inizializzazioni
subcycle_T=0
incr_T=0
granularity=10					#imposto il tic di default: 10 microsec.)
led_time 	= [0.2, 0.2, 0.2, 0.2]
#subcycle_time	= [200, 2000, 50000, 100000]	#moltiplicare per granularity (default: 10 microsecondi)
						#subcycle time 200us is too small (min=3000us)

subcycle_time	= [3000, 5000, 100000, 150000]	#moltiplicare per granularity (default: 10 microsecondi)
						#(in millisec. sono: 20ms, 200ms, 5sec, 10sec)

#pulse_start	= [200, 20, 50, 100]		#_start=200*100 microsec=20 msec.
#pulse_width	= [100, 500, 1000, 5000]	#_width=100*100 microsec=10 msec.
pulse_start	= [0, 0, 0, 0]			#_start=0*10 microsec=0 msec.
pulse_width	= [0, 0, 0, 0]			#_width=0*10 microsec=0 msec.
#incr_impulso	= [10, 10, 10, 10]

canale_dma	= [0, 1, 2, 3]			#ce ne sono 15 (0-14)
gpio_port	= [18, 23, 24, 25]		#porte GPIO (lato pin pari)
#frequency	= [500, 50, 2, 1]		#in Hz

#set della granularity (è il default durante l'inizializzazione tic di incremento in microsecondi)
PWM.setup(granularity, 0)			#default: pulse_incr_us=10, delay_hw=0

for i in canale_dma:
	PWM.init_channel(i, subcycle_time[i])	#canale DMA con tempo subcycle
#	PWM.setup(granularity, 0)		#default: pulse_incr_us=10, delay_hw=0
	#aggiungo un impulso nel canale DMA all'interno di ogni subcycle per ogni GPIO
	#POSSO ANCHE NON AGGIUNGERE NIENTE :-), VOLENDO.
	PWM.add_channel_pulse(i, gpio_port[i], pulse_start[i], pulse_width[i])
#setup per output su GPIO
for i in gpio_port:
	RPIO.setup(i, RPIO.OUT)

for i in canale_dma:
	PWM.print_channel(i) 
	if PWM.is_channel_initialized(i):
		print ("canale ", i, " inizializzato")
	else:
		print ("canale ", i, " NON inizializzato")
	if PWM.is_setup():
		print ("setup canale ", i, "chiamato")
	else:
		print ("setup canale ", i, " NON chiamato")

try:
    while True:
	# LED per vedere se tutto funziona
	for t in led_time:
		for i in gpio_port:
			RPIO.output(i, RPIO.HIGH)
			sleep(t)
			RPIO.output(i, RPIO.LOW)
			sleep(t)
	for d in canale_dma:
		subcycle_T = PWM.get_channel_subcycle_time_us(d)
		incr_T = PWM.get_pulse_incr_us()
		print("CANALE ", d, "subcycle_T =", subcycle_T, "--- incr_T =", incr_T)
        sleep(2)
#    	if PWM.is_setup():	#è stato fatto il setup d'inizializzazione 
#		granularity=granularity*10	#se sì: incremento la granularity
#    		PWM.setup(granularity,0)	#rifaccio il setup

except KeyboardInterrupt:
    pass
    for i in canale_dma:
    	PWM.clear_channel(i)
    	PWM.clear_channel_gpio(i,gpio_port(i))
    PWM.cleanup()
    print "STOP!"
    print "Ciao!"




