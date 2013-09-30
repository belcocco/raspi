#!/usr/bin/env python
# -*- coding: latin-1 *-*
# -*- coding: cp1252 -*-
#Raspberry Pi - GPIO interface
#Sensore di temperatura DS18B40
import os
import glob
import time

import RPi.GPIO as GPIO
from time import sleep
################################### Inizializzazioni
#Carica i moduli necessari al DS18B20
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
#Set per GPIO output
GPIO.cleanup()
GPIO.setmode(GPIO.BCM)
ledOnTemp=False
ledPinsTemp=[24,23,18]  # 3 Led per allarme temperatura
for a in ledPinsTemp:
        GPIO.setup(a,GPIO.OUT)
        GPIO.output(a, False)   #Spegne i 3 led
        sleep(0.1)
     
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'
     
def read_temp_raw():
	f = open(device_file, 'r')
	lines = f.readlines()
	f.close()
	return lines

#Se la def di cui sopra NON dovesse funzionare, sostituire con quanto segue:
#    def read_temp_raw():
#    	catdata = subprocess.Popen(['cat',device_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#    	out,err = catdata.communicate()
#    	out_decode = out.decode('utf-8')
#    	lines = out_decode.split('\n')
#    	return lines
     
def read_temp():
	lines = read_temp_raw()
	while lines[0].strip()[-3:] != 'YES':
		time.sleep(0.2)
		lines = read_temp_raw()
	equals_pos = lines[1].find('t=')
	if equals_pos != -1:
		temp_string = lines[1][equals_pos+2:]
		temp_c = float(temp_string) / 1000.0
		temp_f = temp_c * 9.0 / 5.0 + 32.0

	        #Accendi tutti i led
		if temp_c >= 28:
        	        for a in ledPinsTemp:
                	        GPIO.output(a, True)
                                sleep(0.1)
                                ledOnTemp=False
                #Spegne tutti i led
        	else:
                	for a in ledPinsTemp:
                        	GPIO.output(a, False)
                        	sleep(0.1)
                        	ledOnTemp=False
		return temp_c, temp_f
while True:
	print(read_temp())
	time.sleep(1)
