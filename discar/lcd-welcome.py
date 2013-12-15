#!/usr/bin/env python
# -*- coding: latin-1 *-*
# -*- coding: cp1252 -*-
# Raspberry Pi
# file: lcd-welcome.py
# Python-SMBus and LCD-Display 20x4 (HD44780)
#
# Dic 2013
#Sensore di temperatura DS18B40
#Quando la Temperatura supera i 26 °C la ventola è in funzione.
#Se la temperatura scende al di sotto dei 26 °C la ventola di raffreddamento viene fermata.
#E' obbligatorio collegare con il cavo il GPIO 4 con il pin di mezzo del componente.
#Il GPIO 4 viene utilizzato dai driver per leggere le temperature.
#SOLO così funziona !!!
import os
import glob
import time
import RPIO
################################### Inizializzazioni
#Carica i moduli necessari al DS18B20
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
#Set per GPIO output
RPIO.setmode(RPIO.BCM)
temperatura=25.687
ledOnTemp=False
ledPinsTemp=[24,23]  # 2 Led per segnalazione allarme temperatura
ledPWM=18
RPIO.setup(ledPWM,RPIO.OUT)
RPIO.output(ledPWM, False)   #Spegne la ventola perchè siamo all'inizio
for a in ledPinsTemp:
        RPIO.setup(a,RPIO.OUT)
        RPIO.output(a, False)   #Spegne i 2 led
        time.sleep(0.1)

base_dir_temp = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir_temp + '28*')[0]
sensor_temp_file = device_folder + '/w1_slave'


# I2C address of LCD-Display HD44780 is: 0x27
from ast import literal_eval
import lcddriver1
from subprocess import *
import time

lcd = lcddriver1.lcd()

lcd.lcd_display_string("********************", 1)
lcd.lcd_display_string("* Welcome to Raspi *", 2)
lcd.lcd_display_string("*  DISCAR  Device  *", 3)
lcd.lcd_display_string("********************", 4)

time.sleep(5)

lcd.lcd_display_string("                    ", 1)
lcd.lcd_display_string("                    ", 2)
lcd.lcd_display_string("                    ", 3)
lcd.lcd_display_string("                    ", 4)

#read IP address
cmd = "ip addr show eth0 | grep inet | awk '{print $2}' | cut -d/ -f1"

def run_cmd(cmd):
         p = Popen(cmd, shell=True, stdout=PIPE)
         output = p.communicate()[0]
         return output
 
#read date & time from RTC
base_dir_rtc = '/sys/class/i2c-adapter/i2c-1/1-0068/rtc/rtc0'
RTC_date_file = base_dir_rtc + '/date'
RTC_time_file = base_dir_rtc + '/time'

def read_date_raw():
        f = open(RTC_date_file, 'r')
        date_lines = f.readlines()
        f.close()
        return date_lines

def read_time_raw():
        f = open(RTC_time_file, 'r')
        time_lines = f.readlines()
        f.close()
        return time_lines

def read_temp_raw():
        f = open(sensor_temp_file, 'r')
        temp_lines = f.readlines()
        f.close()
        return temp_lines

#Se la def di cui sopra NON dovesse funzionare, sostituire con quanto segue:
#    def read_temp_raw():
#       catdata = subprocess.Popen(['cat',device_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#       out,err = catdata.communicate()
#       out_decode = out.decode('utf-8')
#       lines = out_decode.split('\n')
#       return lines

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

                #Accendi e spegni ritmicamente tutti i led in caso di allarme (superamento soglia di temperatura)
                if temp_c >= temperatura:
                        for a in ledPinsTemp:
                                RPIO.output(a, True)
                                time.sleep(0.1)
                                ledOnTemp=False
                        RPIO.output(ledPWM, True) #Accende la ventola per raffreddare
                        #time.sleep(0.3)
                        for a in ledPinsTemp:
                                RPIO.output(a, False)
                                time.sleep(0.1)
                                ledOnTemp=False
                #Spegne tutti i led ed accende la ventola per il raffreddamento
                else:
                        for a in ledPinsTemp:
                                RPIO.output(a, False)
                                time.sleep(0.1)
                                ledOnTemp=False
                        RPIO.output(ledPWM, False) #Spegne la ventola perchè la temperatura è sotto soglia
                return temp_c#, temp_f

############################## LOOP PRINCIPALE
try:
        ip_addr = run_cmd(cmd)
        ip_addr = "  IP: " + ip_addr.rstrip("\n") + "   "
        print ip_addr
        lcd.lcd_display_string(ip_addr, 2)      #display ip address on line 2

        while True:
                date_raw = read_date_raw()	#read date (as List from file)
                time_raw = read_time_raw()	#read time (as List from file)
                date_pure = date_raw[0]
                time_pure = time_raw[0]
                date_time = date_pure.strip("\n") + "  " + time_pure.strip("\n")
                temp_c_raw = read_temp()	#read temp (as float from file)
                temp_c_ = repr(temp_c_raw)       #convert to string
                temp_c_pure = "   Temp.-->" + temp_c_[:4]	#only one decimal
# DEBUG                print date_time, "Temp.:",temp_c_pure
                #Visualizza data e ora
                lcd.lcd_display_string(date_time, 1)
                lcd.lcd_display_string(temp_c_pure , 3)
                lcd.lcd_display_string("  Premi Tasto Rosso ", 4)
                time.sleep(1)
#try:
#        while True:
#                print(read_temp())
#                time.sleep(1)



except KeyboardInterrupt:
        print " "
        print "Ciao !"
#        RPIO.cleanup()
#RPIO.cleanup()


