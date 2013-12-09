#!/usr/bin/env python
# -*- coding: latin-1 *-*
# -*- coding: cp1252 -*-
#Raspberry Pi - GPIO interface with RPIO Interrupt Python module
import RPIO, time, datetime

# http://elinux.org/RPi_Low-level_peripherals#P5_header
# P5 header: pin nearest outer corner of board (and J1.1) is P5.1 (Port 5 Pin 1)
# 1: +5V    2: +3.3 V
# 3: GP28   4: GP29
# 5: GP30   6: GP31
# 7: GND    8: GND

# http://elinux.org/RPi_Low-level_peripherals#General_Purpose_Input.2FOutput_.28GPIO.29
# P1 header: pin at corner of board is pin 2. Pin 1 is towards microUSB power connector
# P1 header 2-26: 5V0 5V0 GND  14  15 18  GND  23  24 GND  25  08  07
# P1 header 1-25: 3V3 02  03  04 GND 17 27 22 3V3  10  09  11 GND

#------------------INIZIALIZZAZIONI
#Canali su pin PARI
INT7 = 7      # define GPIO number 7 for interrupt from IC
INT8 = 8      # define GPIO number 8 for interrupt from IC
INT25 = 25      # define GPIO number 25 for interrupt from IC
INT24 = 24      # define GPIO number 24 for interrupt from IC
INT23 = 23      # define GPIO number 23 for interrupt from IC
INT18 = 18      # define GPIO number 18 for interrupt from IC (PWM)

#Canali su pin DISPARI
INT11 = 11      # define GPIO number 11 for interrupt from IC 
INT9 = 9      # define GPIO number 9 for interrupt from IC
INT10 = 10      # define GPIO number 10 for interrupt from IC
INT22 = 22      # define GPIO number 22 for interrupt from IC
INT27 = 27      # define GPIO number 27 for interrupt from IC
INT17 = 17      # define GPIO number 17 for interrupt from IC

#Canali speciali
INT4 = 4      # define GPIO number 4 for interrupt from IC (DS18B20 - Sensore di Temperatura)
INT3 = 3      # define GPIO number 3 for interrupt from IC (SCL-i2c)
INT2 = 2      # define GPIO number 2 for interrupt from IC (SDA-i2c)

#Canali per UART
INT14 = 14      # define GPIO number 14 for interrupt from IC (UART Tx)
INT15 = 15      # define GPIO number 15 for interrupt from IC (UART Rx)

lastTime = time.time()
dMax1 = 0;
dMin1 = 2;
dSum1 = 0;
dCount1 = 0;
dAvg1 = 0;
dFirst1 = 1;

dMax2 = 0;
dMin2 = 2;
dSum2 = 0;
dCount2 = 0;
dAvg2 = 0;
dFirst2 = 1;

# set up input channel with pull-up control. Can be PUD_UP, PUD_DOWN or PUD_OFF (default)
#Tutti i canali sono settati in ingresso, quando serve  settare l'output da programma
RPIO.setup(INT7, RPIO.IN, pull_up_down=RPIO.PUD_UP)
RPIO.setup(INT8, RPIO.IN, pull_up_down=RPIO.PUD_UP)
RPIO.setup(INT25, RPIO.IN, pull_up_down=RPIO.PUD_UP)
RPIO.setup(INT24, RPIO.IN, pull_up_down=RPIO.PUD_UP)
RPIO.setup(INT23, RPIO.IN, pull_up_down=RPIO.PUD_UP)
RPIO.setup(INT18, RPIO.IN, pull_up_down=RPIO.PUD_UP)

RPIO.setup(INT11, RPIO.IN, pull_up_down=RPIO.PUD_UP)
RPIO.setup(INT9, RPIO.IN, pull_up_down=RPIO.PUD_UP)
RPIO.setup(INT10, RPIO.IN, pull_up_down=RPIO.PUD_UP)
RPIO.setup(INT22, RPIO.IN, pull_up_down=RPIO.PUD_UP)
RPIO.setup(INT27, RPIO.IN, pull_up_down=RPIO.PUD_UP)
RPIO.setup(INT17, RPIO.IN, pull_up_down=RPIO.PUD_UP)

RPIO.setup(INT4, RPIO.IN, pull_up_down=RPIO.PUD_UP)
RPIO.setup(INT3, RPIO.IN, pull_up_down=RPIO.PUD_UP)
RPIO.setup(INT2, RPIO.IN, pull_up_down=RPIO.PUD_UP)

RPIO.setup(INT14, RPIO.IN, pull_up_down=RPIO.PUD_UP)
RPIO.setup(INT15, RPIO.IN, pull_up_down=RPIO.PUD_UP)

# read all input from gpio
input_value_7 = RPIO.input(INT7)
input_value_8 = RPIO.input(INT8)
input_value_25 = RPIO.input(INT25)
input_value_24 = RPIO.input(INT24)
input_value_23 = RPIO.input(INT23)
input_value_18 = RPIO.input(INT18)

input_value_11 = RPIO.input(INT7)
input_value_9 = RPIO.input(INT9)
input_value_10 = RPIO.input(INT10)
input_value_22 = RPIO.input(INT22)
input_value_27 = RPIO.input(INT27)
input_value_17 = RPIO.input(INT17)

input_value_4 = RPIO.input(INT4)
input_value_3 = RPIO.input(INT3)
input_value_2 = RPIO.input(INT2)

input_value_14 = RPIO.input(INT14)
input_value_15 = RPIO.input(INT15)

#Definizione della callback per impulsi da pin-IC collegato a GPIO 7
def gpio_callback_INT7(gpio_id, val):
#   input_value_7 = RPIO.input(INT7)
#   print("INT7: ", input_value_7)
   global lastTime1, dMax1, dMin1, dSum1, dCount1, dFirst1
   now1 = datetime.datetime.now()
   dstr1 = str(now1.strftime("%H:%M:%S.%f"))
   nowTime1 = time.time()
   if (dFirst1 == 1):
      dFirst1 = 0;
      lastTime1 = nowTime1;
   else:
      dTime1 = nowTime1 - lastTime1
      lastTime1 = nowTime1
      if (dTime1 > dMax1):
         dMax1 = dTime1
      if (dTime1 < dMin1):
         dMin1 = dTime1
      dCount1 += 1
      dSum1 += dTime1
      #stampa ogni tic
      print("CB-7: ---------------> gpio %s: %s at %s delta: %08.6f" % (gpio_id, val, dstr1, dTime1))

#Definizione della callback per impulsi da pin-IC collegato a GPIO 8
def gpio_callback_INT8(gpio_id, val):
   input_value_8 = RPIO.input(INT8)
   print("INT8: ", input_value_8)

      #stampa tic 4017
#      print("CB-2: ---------------> gpio %s: %s at %s delta: %08.6f" % (gpio_id, val, dstr2, dTime2))

#Definizione della callback per impulsi da pin-IC collegato a GPIO 25
def gpio_callback_INT25(gpio_id, val):
   global lastTime1, dMax1, dMin1, dSum1, dCount1, dFirst1
   now1 = datetime.datetime.now()
   dstr1 = str(now1.strftime("%H:%M:%S.%f"))
   nowTime1 = time.time()
   if (dFirst1 == 1):
      dFirst1 = 0;
      lastTime1 = nowTime1;
   else:
      dTime1 = nowTime1 - lastTime1
      lastTime1 = nowTime1      
      if (dTime1 > dMax1):
         dMax1 = dTime1
      if (dTime1 < dMin1):
         dMin1 = dTime1
      dCount1 += 1
      dSum1 += dTime1
      #stampa ogni tic in uscita da (3) su 555
#      print("CB-1: ---------------> gpio %s: %s at %s delta: %08.6f" % (gpio_id, val, dstr1, dTime1))

#Definizione della callback per impulsi da pin-IC collegato a GPIO 24
def gpio_callback_INT24(gpio_id, val):
   global lastTime2, dMax2, dMin2, dSum2, dCount2, dFirst2
   now2 = datetime.datetime.now()
   dstr2 = str(now2.strftime("%H:%M:%S.%f"))
   nowTime2 = time.time()
   if (dFirst2 == 1):
      dFirst2 = 0;
      lastTime2 = nowTime2;
   else:
      dTime2 = nowTime2 - lastTime2
      lastTime2 = nowTime2
      if (dTime2 > dMax2):
         dMax2 = dTime2
      if (dTime2 < dMin2):
         dMin2 = dTime2
      dCount2 += 1
      dSum2 += dTime2
      #stampa tic 4017
#      print("CB-2: ---------------> gpio %s: %s at %s delta: %08.6f" % (gpio_id, val, dstr2, dTime2))

#Definizione della callback per impulsi da pin-IC collegato a GPIO 23
def gpio_callback_INT23(gpio_id, val):
   global lastTime1, dMax1, dMin1, dSum1, dCount1, dFirst1
   now1 = datetime.datetime.now()
   dstr1 = str(now1.strftime("%H:%M:%S.%f"))
   nowTime1 = time.time()
   if (dFirst1 == 1):
      dFirst1 = 0;
      lastTime1 = nowTime1;
   else:
      dTime1 = nowTime1 - lastTime1
      lastTime1 = nowTime1      
      if (dTime1 > dMax1):
         dMax1 = dTime1
      if (dTime1 < dMin1):
         dMin1 = dTime1
      dCount1 += 1
      dSum1 += dTime1
      #stampa ogni tic in uscita da (3) su 555
#      print("CB-1: ---------------> gpio %s: %s at %s delta: %08.6f" % (gpio_id, val, dstr1, dTime1))

#Definizione della callback per impulsi da pin-IC collegato a GPIO 18
def gpio_callback_INT18(gpio_id, val):
   global lastTime2, dMax2, dMin2, dSum2, dCount2, dFirst2
   now2 = datetime.datetime.now()
   dstr2 = str(now2.strftime("%H:%M:%S.%f"))
   nowTime2 = time.time()
   if (dFirst2 == 1):
      dFirst2 = 0;
      lastTime2 = nowTime2;
   else:
      dTime2 = nowTime2 - lastTime2
      lastTime2 = nowTime2
      if (dTime2 > dMax2):
         dMax2 = dTime2
      if (dTime2 < dMin2):
         dMin2 = dTime2
      dCount2 += 1
      dSum2 += dTime2
      #stampa tic 4017
#      print("CB-2: ---------------> gpio %s: %s at %s delta: %08.6f" % (gpio_id, val, dstr2, dTime2))

#Definizione della callback per impulsi da pin-IC collegato a GPIO 11
def gpio_callback_INT11(gpio_id, val):
   global lastTime1, dMax1, dMin1, dSum1, dCount1, dFirst1
   now1 = datetime.datetime.now()
   dstr1 = str(now1.strftime("%H:%M:%S.%f"))
   nowTime1 = time.time()
   if (dFirst1 == 1):
      dFirst1 = 0;
      lastTime1 = nowTime1;
   else:
      dTime1 = nowTime1 - lastTime1
      lastTime1 = nowTime1      
      if (dTime1 > dMax1):
         dMax1 = dTime1
      if (dTime1 < dMin1):
         dMin1 = dTime1
      dCount1 += 1
      dSum1 += dTime1
      #stampa ogni tic in uscita da (3) su 555
#      print("CB-1: ---------------> gpio %s: %s at %s delta: %08.6f" % (gpio_id, val, dstr1, dTime1))

#Definizione della callback per impulsi da pin-IC collegato a GPIO 9
def gpio_callback_INT9(gpio_id, val):
   global lastTime2, dMax2, dMin2, dSum2, dCount2, dFirst2
   now2 = datetime.datetime.now()
   dstr2 = str(now2.strftime("%H:%M:%S.%f"))
   nowTime2 = time.time()
   if (dFirst2 == 1):
      dFirst2 = 0;
      lastTime2 = nowTime2;
   else:
      dTime2 = nowTime2 - lastTime2
      lastTime2 = nowTime2
      if (dTime2 > dMax2):
         dMax2 = dTime2
      if (dTime2 < dMin2):
         dMin2 = dTime2
      dCount2 += 1
      dSum2 += dTime2
      #stampa tic 4017
#      print("CB-2: ---------------> gpio %s: %s at %s delta: %08.6f" % (gpio_id, val, dstr2, dTime2))

#Definizione della callback per impulsi da pin-IC collegato a GPIO 10
def gpio_callback_INT10(gpio_id, val):
   global lastTime1, dMax1, dMin1, dSum1, dCount1, dFirst1
   now1 = datetime.datetime.now()
   dstr1 = str(now1.strftime("%H:%M:%S.%f"))
   nowTime1 = time.time()
   if (dFirst1 == 1):
      dFirst1 = 0;
      lastTime1 = nowTime1;
   else:
      dTime1 = nowTime1 - lastTime1
      lastTime1 = nowTime1      
      if (dTime1 > dMax1):
         dMax1 = dTime1
      if (dTime1 < dMin1):
         dMin1 = dTime1
      dCount1 += 1
      dSum1 += dTime1
      #stampa ogni tic in uscita da (3) su 555
#      print("CB-1: ---------------> gpio %s: %s at %s delta: %08.6f" % (gpio_id, val, dstr1, dTime1))

#Definizione della callback per impulsi da pin-IC collegato a GPIO 22
def gpio_callback_INT22(gpio_id, val):
   global lastTime2, dMax2, dMin2, dSum2, dCount2, dFirst2
   now2 = datetime.datetime.now()
   dstr2 = str(now2.strftime("%H:%M:%S.%f"))
   nowTime2 = time.time()
   if (dFirst2 == 1):
      dFirst2 = 0;
      lastTime2 = nowTime2;
   else:
      dTime2 = nowTime2 - lastTime2
      lastTime2 = nowTime2
      if (dTime2 > dMax2):
         dMax2 = dTime2
      if (dTime2 < dMin2):
         dMin2 = dTime2
      dCount2 += 1
      dSum2 += dTime2
      #stampa tic 4017
#      print("CB-2: ---------------> gpio %s: %s at %s delta: %08.6f" % (gpio_id, val, dstr2, dTime2))

#Definizione della callback per impulsi da pin-IC collegato a GPIO 27
def gpio_callback_INT27(gpio_id, val):
   global lastTime1, dMax1, dMin1, dSum1, dCount1, dFirst1
   now1 = datetime.datetime.now()
   dstr1 = str(now1.strftime("%H:%M:%S.%f"))
   nowTime1 = time.time()
   if (dFirst1 == 1):
      dFirst1 = 0;
      lastTime1 = nowTime1;
   else:
      dTime1 = nowTime1 - lastTime1
      lastTime1 = nowTime1      
      if (dTime1 > dMax1):
         dMax1 = dTime1
      if (dTime1 < dMin1):
         dMin1 = dTime1
      dCount1 += 1
      dSum1 += dTime1
      #stampa ogni tic in uscita da (3) su 555
#      print("CB-1: ---------------> gpio %s: %s at %s delta: %08.6f" % (gpio_id, val, dstr1, dTime1))

#Definizione della callback per impulsi da pin-IC collegato a GPIO 17
def gpio_callback_INT17(gpio_id, val):
   global lastTime2, dMax2, dMin2, dSum2, dCount2, dFirst2
   now2 = datetime.datetime.now()
   dstr2 = str(now2.strftime("%H:%M:%S.%f"))
   nowTime2 = time.time()
   if (dFirst2 == 1):
      dFirst2 = 0;
      lastTime2 = nowTime2;
   else:
      dTime2 = nowTime2 - lastTime2
      lastTime2 = nowTime2
      if (dTime2 > dMax2):
         dMax2 = dTime2
      if (dTime2 < dMin2):
         dMin2 = dTime2
      dCount2 += 1
      dSum2 += dTime2
      #stampa tic 4017
#      print("CB-2: ---------------> gpio %s: %s at %s delta: %08.6f" % (gpio_id, val, dstr2, dTime2))

#Definizione della callback per impulsi da pin-IC collegato a GPIO 4
def gpio_callback_INT4(gpio_id, val):
   global lastTime1, dMax1, dMin1, dSum1, dCount1, dFirst1
   now1 = datetime.datetime.now()
   dstr1 = str(now1.strftime("%H:%M:%S.%f"))
   nowTime1 = time.time()
   if (dFirst1 == 1):
      dFirst1 = 0;
      lastTime1 = nowTime1;
   else:
      dTime1 = nowTime1 - lastTime1
      lastTime1 = nowTime1      
      if (dTime1 > dMax1):
         dMax1 = dTime1
      if (dTime1 < dMin1):
         dMin1 = dTime1
      dCount1 += 1
      dSum1 += dTime1
      #stampa ogni tic in uscita da (3) su 555
#      print("CB-1: ---------------> gpio %s: %s at %s delta: %08.6f" % (gpio_id, val, dstr1, dTime1))

#Definizione della callback per impulsi da pin-IC collegato a GPIO 3
def gpio_callback_INT3(gpio_id, val):
   global lastTime2, dMax2, dMin2, dSum2, dCount2, dFirst2
   now2 = datetime.datetime.now()
   dstr2 = str(now2.strftime("%H:%M:%S.%f"))
   nowTime2 = time.time()
   if (dFirst2 == 1):
      dFirst2 = 0;
      lastTime2 = nowTime2;
   else:
      dTime2 = nowTime2 - lastTime2
      lastTime2 = nowTime2
      if (dTime2 > dMax2):
         dMax2 = dTime2
      if (dTime2 < dMin2):
         dMin2 = dTime2
      dCount2 += 1
      dSum2 += dTime2
      #stampa tic 4017
#      print("CB-2: ---------------> gpio %s: %s at %s delta: %08.6f" % (gpio_id, val, dstr2, dTime2))

#Definizione della callback per impulsi da pin-IC collegato a GPIO 2
def gpio_callback_INT2(gpio_id, val):
   global lastTime1, dMax1, dMin1, dSum1, dCount1, dFirst1
   now1 = datetime.datetime.now()
   dstr1 = str(now1.strftime("%H:%M:%S.%f"))
   nowTime1 = time.time()
   if (dFirst1 == 1):
      dFirst1 = 0;
      lastTime1 = nowTime1;
   else:
      dTime1 = nowTime1 - lastTime1
      lastTime1 = nowTime1      
      if (dTime1 > dMax1):
         dMax1 = dTime1
      if (dTime1 < dMin1):
         dMin1 = dTime1
      dCount1 += 1
      dSum1 += dTime1
      #stampa ogni tic in uscita da (3) su 555
#      print("CB-1: ---------------> gpio %s: %s at %s delta: %08.6f" % (gpio_id, val, dstr1, dTime1))

#Definizione della callback per impulsi da pin-IC collegato a GPIO 14
def gpio_callback_INT14(gpio_id, val):
   global lastTime2, dMax2, dMin2, dSum2, dCount2, dFirst2
   now2 = datetime.datetime.now()
   dstr2 = str(now2.strftime("%H:%M:%S.%f"))
   nowTime2 = time.time()
   if (dFirst2 == 1):
      dFirst2 = 0;
      lastTime2 = nowTime2;
   else:
      dTime2 = nowTime2 - lastTime2
      lastTime2 = nowTime2
      if (dTime2 > dMax2):
         dMax2 = dTime2
      if (dTime2 < dMin2):
         dMin2 = dTime2
      dCount2 += 1
      dSum2 += dTime2
      #stampa tic 4017
#      print("CB-2: ---------------> gpio %s: %s at %s delta: %08.6f" % (gpio_id, val, dstr2, dTime2))

#Definizione della callback per impulsi da pin-IC collegato a GPIO 15
def gpio_callback_INT15(gpio_id, val):
   global lastTime1, dMax1, dMin1, dSum1, dCount1, dFirst1
   now1 = datetime.datetime.now()
   dstr1 = str(now1.strftime("%H:%M:%S.%f"))
   nowTime1 = time.time()
   if (dFirst1 == 1):
      dFirst1 = 0;
      lastTime1 = nowTime1;
   else:
      dTime1 = nowTime1 - lastTime1
      lastTime1 = nowTime1      
      if (dTime1 > dMax1):
         dMax1 = dTime1
      if (dTime1 < dMin1):
         dMin1 = dTime1
      dCount1 += 1
      dSum1 += dTime1
      #stampa ogni tic in uscita da (3) su 555
#      print("CB-1: ---------------> gpio %s: %s at %s delta: %08.6f" % (gpio_id, val, dstr1, dTime1))



# GPIO interrupt callbacks. Note this resets any previous config of pullup resistor
# RPIO.add_interrupt_callback(INTPIN, gpio_callback2, edge='falling',pull_up_down=RPIO.PUD_UP, debounce_timeout_ms=100)
# RPIO.add_interrupt_callback(INTPIN, gpio_callback2, edge='both', pull_up_down=RPIO.PUD_DOWN, debounce_timeout_ms=10)

#Interrupt adatto ad avere un tic ogni 100 msec.
#RPIO.add_interrupt_callback(INTPIN, gpio_callback1, edge='rising', pull_up_down=RPIO.PUD_OFF, debounce_timeout_ms=100)
#Interrupt adatto ad avere un tic ogni 2,87 msec. il massimo che si ottiene con le resistenze scelte
RPIO.add_interrupt_callback(INT7, gpio_callback_INT7, edge='rising', pull_up_down=RPIO.PUD_UP)#, debounce_timeout_ms=100)
#RPIO.add_interrupt_callback(INT8, gpio_callback_INT8, edge='rising', pull_up_down=RPIO.PUD_UP)#, debounce_timeout_ms=100)
#RPIO.add_interrupt_callback(INT25, gpio_callback_INT25, edge='rising', pull_up_down=RPIO.PUD_UP)#, debounce_timeout_ms=100)
#RPIO.add_interrupt_callback(INT24, gpio_callback_INT24, edge='rising', pull_up_down=RPIO.PUD_UP)#, debounce_timeout_ms=100)
#RPIO.add_interrupt_callback(INT23, gpio_callback_INT23, edge='rising', pull_up_down=RPIO.PUD_UP)#, debounce_timeout_ms=100)
#RPIO.add_interrupt_callback(INT18, gpio_callback_INT18, edge='rising', pull_up_down=RPIO.PUD_UP)#, debounce_timeout_ms=100)
#RPIO.add_interrupt_callback(INT11, gpio_callback_INT11, edge='rising', pull_up_down=RPIO.PUD_UP)#, debounce_timeout_ms=100)
#RPIO.add_interrupt_callback(INT9, gpio_callback_INT9, edge='rising', pull_up_down=RPIO.PUD_UP)#, debounce_timeout_ms=100)
#RPIO.add_interrupt_callback(INT10, gpio_callback_INT10, edge='rising', pull_up_down=RPIO.PUD_UP)#, debounce_timeout_ms=100)
#RPIO.add_interrupt_callback(INT22, gpio_callback_INT22, edge='rising', pull_up_down=RPIO.PUD_UP)#, debounce_timeout_ms=100)
#RPIO.add_interrupt_callback(INT27, gpio_callback_INT27, edge='rising', pull_up_down=RPIO.PUD_UP)#, debounce_timeout_ms=100)
#RPIO.add_interrupt_callback(INT17, gpio_callback_INT17, edge='rising', pull_up_down=RPIO.PUD_UP)#, debounce_timeout_ms=100)
#RPIO.add_interrupt_callback(INT4, gpio_callback_INT4, edge='rising', pull_up_down=RPIO.PUD_UP)#, debounce_timeout_ms=100)
#RPIO.add_interrupt_callback(INT3, gpio_callback_INT3, edge='rising', pull_up_down=RPIO.PUD_UP)#, debounce_timeout_ms=100)
#RPIO.add_interrupt_callback(INT2, gpio_callback_INT2, edge='rising', pull_up_down=RPIO.PUD_UP)#, debounce_timeout_ms=100)
#RPIO.add_interrupt_callback(INT14, gpio_callback_INT14, edge='rising', pull_up_down=RPIO.PUD_UP)#, debounce_timeout_ms=100)
#RPIO.add_interrupt_callback(INT15, gpio_callback_INT15, edge='rising', pull_up_down=RPIO.PUD_UP)#, debounce_timeout_ms=100)

# Starts waiting for interrupts (exit with Ctrl+C)
# RPIO.wait_for_interrupts()   # blocks until interrupt, never proceeds beyond this point

RPIO.wait_for_interrupts(threaded=True)   # non-blocking, separate thread

try:
	while (1):
	   	now1 = datetime.datetime.now()
   		dstr1 = str(now1.strftime("%Y-%m-%d_%H:%M:%S"))
   		if (dCount1 > 0):
      			dAvg1 = dSum1 / dCount1
#		print("Time4060: %s Avg: %08.6f Min: %08.6f Max: %08.6f Total: %d" % (dstr1, dAvg1, dMin1, dMax1, dCount1))

#        	now2 = datetime.datetime.now()
#        	dstr2 = str(now2.strftime("%Y-%m-%d_%H:%M:%S"))
#   		if (dCount2 > 0):
#      			dAvg2 = dSum2 / dCount2
#		print("Time4011: %s Avg: %08.6f Min: %08.6f Max: %08.6f Total: %d" % (dstr2, dAvg2, dMin2, dMax2, dCount2))

   		time.sleep(1)  #con (1) Stampa 1 volta ogni secondo
				#con (10) stampa ogni 10 secondi

except KeyboardInterrupt:
        print " "
        print "Ciao !"
        RPIO.cleanup()
RPIO.cleanup()


