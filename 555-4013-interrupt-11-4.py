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

INT555 = 11      # define GPIO pin number for interrupt 555 (pin3) con GPIO 11
INT4013 = 9      # define GPIO pin number for interrupt CD4013 (pin13) con GPIO 9
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

# set up input channel with pull-up control. Can be
# PUD_UP, PUD_DOWN or PUD_OFF (default)
RPIO.setup(INT555, RPIO.IN, pull_up_down=RPIO.PUD_UP)
RPIO.setup(INT4013, RPIO.IN, pull_up_down=RPIO.PUD_UP)

# read input from gpio
input_value_555 = RPIO.input(INT555)
input_value_4013 = RPIO.input(INT4013)

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


# GPIO interrupt callbacks. Note this resets any previous config of pullup resistor
# RPIO.add_interrupt_callback(INTPIN, gpio_callback2, edge='falling',pull_up_down=RPIO.PUD_UP, debounce_timeout_ms=100)
# RPIO.add_interrupt_callback(INTPIN, gpio_callback2, edge='both', pull_up_down=RPIO.PUD_DOWN, debounce_timeout_ms=10)

#Interrupt adatto ad avere un tic ogni 100 msec.
#RPIO.add_interrupt_callback(INTPIN, gpio_callback1, edge='rising', pull_up_down=RPIO.PUD_OFF, debounce_timeout_ms=100)
#Interrupt adatto ad avere un tic ogni 2,87 msec. il massimo che si ottiene con le resistenze scelte
RPIO.add_interrupt_callback(INT555, gpio_callback_1, edge='rising', pull_up_down=RPIO.PUD_UP)#, debounce_timeout_ms=100)
RPIO.add_interrupt_callback(INT4013, gpio_callback_2, edge='rising', pull_up_down=RPIO.PUD_UP)#, debounce_timeout_ms=100)

# Starts waiting for interrupts (exit with Ctrl+C)
# RPIO.wait_for_interrupts()   # blocks until interrupt, never proceeds beyond this point

RPIO.wait_for_interrupts(threaded=True)   # non-blocking, separate thread

try:
	while (1):
	   	now1 = datetime.datetime.now()
   		dstr1 = str(now1.strftime("%Y-%m-%d_%H:%M:%S"))
   		if (dCount1 > 0):
      			dAvg1 = dSum1 / dCount1
		print("Time555: %s Avg: %08.6f Min: %08.6f Max: %08.6f Total: %d" % (dstr1, dAvg1, dMin1, dMax1, dCount1))

        	now2 = datetime.datetime.now()
        	dstr2 = str(now2.strftime("%Y-%m-%d_%H:%M:%S"))
   		if (dCount2 > 0):
      			dAvg2 = dSum2 / dCount2
		print("Time4013: %s Avg: %08.6f Min: %08.6f Max: %08.6f Total: %d" % (dstr2, dAvg2, dMin2, dMax2, dCount2))

   		time.sleep(1)  #10) Stampa 1 volta ogni secondo 

except KeyboardInterrupt:
        print " "
        print "Ciao !"
        RPIO.cleanup()
RPIO.cleanup()


