#!/usr/bin/env python
# -*- coding: latin-1 *-*
# -*- coding: cp1252 -*-
#Raspberry Pi - GPIO interface with RPIO Interrupt Python Module
#In this demo are used four IC: 
#1) Timer 555
#2) Dual Flip-Flop CD4013
#3) Decade Counter/Divider with 10 decoded outputs CD4017
#4) Moltiplicatore di frequenza con Phase-Locked Loop CD4046

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

INT555 = 11      # define GPIO number for interrupt 555 (pin3) - Raspi input GPIO 11
INT4013 = 9      # define GPIO number for interrupt 4013 (pin13) - Raspi input GPIO 9
INT4017 = 7      # define GPIO number for interrupt 4017 (pin12) - Raspi input GPIO 7
INT4046 = 4      # define GPIO number for interrupt 4046 (pin4) - Raspi input GPIO 4 
lastTime = time.time()
dMax1 = 0; dMin1 = 2; dSum1 = 0; dCount1 = 0; dAvg1 = 1; dFirst1 = 1; #555
dMax2 = 0; dMin2 = 2; dSum2 = 0; dCount2 = 0; dAvg2 = 1; dFirst2 = 1; #4013
dMax3 = 0; dMin3 = 2; dSum3 = 0; dCount3 = 0; dAvg3 = 1; dFirst3 = 1; #4017
dMax4 = 0; dMin4 = 2; dSum4 = 0; dCount4 = 0; dAvg4 = 1; dFirst4 = 1; #4046

# set up input channel with pull-up control. Can be
# PUD_UP, PUD_DOWN or PUD_OFF (default)
RPIO.setup(INT555, RPIO.IN, pull_up_down=RPIO.PUD_UP)
RPIO.setup(INT4013, RPIO.IN, pull_up_down=RPIO.PUD_UP)
RPIO.setup(INT4017, RPIO.IN, pull_up_down=RPIO.PUD_UP)
RPIO.setup(INT4046, RPIO.IN, pull_up_down=RPIO.PUD_UP)

# read input from gpio
input_value_11 = RPIO.input(INT555)
input_value_4 = RPIO.input(INT4013)
input_value_11 = RPIO.input(INT4017)
input_value_4 = RPIO.input(INT4046)

#Definizione della callback per impulsi in uscita da pin 3 su 555 (collegato a GPIO 11)
def gpio_callback_1(gpio_id, val):
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

#Definizione della callback per impulsi in uscita da 4013 su pin 13 (collegato a GPIO 9)
def gpio_callback_2(gpio_id, val):
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
      #stampa tic 4013
#      print("CB-2: ---------------> gpio %s: %s at %s delta: %08.6f" % (gpio_id, val, dstr2, dTime2))

#Definizione della callback per impulsi in uscita da 4017 su pin 12 (collegato a GPIO 7)
def gpio_callback_3(gpio_id, val):
   global lastTime3, dMax3, dMin3, dSum3, dCount3, dFirst3
   now3 = datetime.datetime.now()
   dstr3 = str(now3.strftime("%H:%M:%S.%f"))
   nowTime3 = time.time()
   if (dFirst3 == 1):
      dFirst3 = 0;
      lastTime3 = nowTime3;
   else:
      dTime3 = nowTime3 - lastTime3
      lastTime3 = nowTime3
      if (dTime3 > dMax3):
         dMax3 = dTime3
      if (dTime3 < dMin3):
         dMin3 = dTime3
      dCount3 += 1
      dSum3 += dTime3
      #stampa tic 4017
#      print("CB-3: ---------------> gpio %s: %s at %s delta: %08.6f" % (gpio_id, val, dstr3, dTime3))

#Definizione della callback per impulsi in uscita da 4046 su pin 4 (collegato a GPIO 4)
def gpio_callback_4(gpio_id, val):
   global lastTime4, dMax4, dMin4, dSum4, dCount4, dFirst4
   now4 = datetime.datetime.now()
   dstr4 = str(now4.strftime("%H:%M:%S.%f"))
   nowTime4 = time.time()
   if (dFirst4 == 1):
      dFirst4 = 0;
      lastTime4 = nowTime4;
   else:
      dTime4 = nowTime4 - lastTime4
      lastTime4 = nowTime4
      if (dTime4 > dMax4):
         dMax4 = dTime4
      if (dTime4 < dMin4):
         dMin4 = dTime4
      dCount4 += 1
      dSum4 += dTime4
      #stampa tic 4046
#      print("CB-4: ---------------> gpio %s: %s at %s delta: %08.6f" % (gpio_id, val, dstr4, dTime4))

# GPIO interrupt callbacks. Note this resets any previous config of pullup resistor
# RPIO.add_interrupt_callback(INTPIN, gpio_callback2, edge='falling',pull_up_down=RPIO.PUD_UP, debounce_timeout_ms=100)
# RPIO.add_interrupt_callback(INTPIN, gpio_callback2, edge='both', pull_up_down=RPIO.PUD_DOWN, debounce_timeout_ms=10)

#Interrupt adatto ad avere un tic ogni 100 msec.
#RPIO.add_interrupt_callback(INTPIN, gpio_callback1, edge='rising', pull_up_down=RPIO.PUD_OFF, debounce_timeout_ms=100)
#Interrupt adatto ad avere un tic ogni 2,87 msec. il massimo che si ottiene con le resistenze scelte
RPIO.add_interrupt_callback(INT555, gpio_callback_1, edge='rising', pull_up_down=RPIO.PUD_UP)#, debounce_timeout_ms=100)
RPIO.add_interrupt_callback(INT4013, gpio_callback_2, edge='rising', pull_up_down=RPIO.PUD_UP)#, debounce_timeout_ms=100)
RPIO.add_interrupt_callback(INT4017, gpio_callback_3, edge='rising', pull_up_down=RPIO.PUD_UP)#, debounce_timeout_ms=100)
RPIO.add_interrupt_callback(INT4046, gpio_callback_4, edge='rising', pull_up_down=RPIO.PUD_UP)#, debounce_timeout_ms=100)

# Starts waiting for interrupts (exit with Ctrl+C)
# RPIO.wait_for_interrupts()   # blocks until interrupt, never proceeds beyond this point

RPIO.wait_for_interrupts(threaded=True)   # non-blocking, separate thread

try:
	while (1):
	   	now1 = datetime.datetime.now()
   		dstr1 = str(now1.strftime("%Y-%m-%d_%H:%M:%S"))
   		if (dCount1 > 0):
      			dAvg1 = dSum1 / dCount1
#		print("Time555: %s Avg: %08.6f Min: %08.6f Max: %08.6f Tic: %d" % (dstr1, dAvg1, dMin1, dMax1, dCount1))

        	now2 = datetime.datetime.now()
        	dstr2 = str(now2.strftime("%Y-%m-%d_%H:%M:%S"))
   		if (dCount2 > 0):
      			dAvg2 = dSum2 / dCount2
		print("Time4013: %s Avg: %08.6f Min: %08.6f Max: %08.6f Tic: %d" % (dstr2, dAvg2, dMin2, dMax2, dCount2))

                now3 = datetime.datetime.now()
                dstr3 = str(now3.strftime("%Y-%m-%d_%H:%M:%S"))
                if (dCount3 > 0):
                        dAvg3 = dSum3 / dCount3
#                print("Time4017: %s Avg: %08.6f Min: %08.6f Max: %08.6f Tic: %d" % (dstr3, dAvg3, dMin3, dMax3, dCount3))

                now4 = datetime.datetime.now()
                dstr4 = str(now4.strftime("%Y-%m-%d_%H:%M:%S"))
                if (dCount4 > 0):
                        dAvg4 = dSum4 / dCount4
#                print("Time4046: %s Avg: %08.6f Min: %08.6f Max: %08.6f Tic: %d" % (dstr4, dAvg4, dMin4, dMax4, dCount4))
#		print(" ")

   		time.sleep(1)  #10) #Stampa 1 volta ogni secondo 

except KeyboardInterrupt:
        print " "
        print "Ciao !"
        RPIO.cleanup()
RPIO.cleanup()


