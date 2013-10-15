#!/usr/bin/python
# RPIO Documentation: http://pythonhosted.org/RPIO
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
# P1 header 1-25: 3V3 0/2 1/3  04 GND 17 12/27 22 3V3  10  09  11 GND

INTPIN = 11      # define GPIO pin number for interrupt test
lastTime = time.time()
dMax = 0;
dMin = 2;
dSum = 0;
dCount = 0;
dAvg = 0;
dFirst = 1;

# set up input channel with pull-up control. Can be
# PUD_UP, PUD_DOWN or PUD_OFF (default)
RPIO.setup(INTPIN, RPIO.IN, pull_up_down=RPIO.PUD_UP)

# read input from gpio
input_value = RPIO.input(INTPIN)

def gpio_callback1(gpio_id, val):
   global lastTime, dMax, dMin, dSum, dCount, dFirst
   now = datetime.datetime.now()
   dstr = str(now.strftime("%H:%M:%S.%f"))
   nowTime = time.time()
   if (dFirst == 1):
      dFirst = 0;
      lastTime = nowTime;
   else:
      dTime = nowTime - lastTime
      lastTime = nowTime      
      if (dTime > dMax):
         dMax = dTime
      if (dTime < dMin):
         dMin = dTime
      dCount += 1
      dSum += dTime
      #stampa ogni tic
#      print("CB1: gpio %s: %s at %s delta: %08.6f" % (gpio_id, val, dstr, dTime))

# GPIO interrupt callbacks. Note this resets any previous config of pullup resistor
# RPIO.add_interrupt_callback(INTPIN, gpio_callback2, edge='falling',pull_up_down=RPIO.PUD_UP, debounce_timeout_ms=100)
# RPIO.add_interrupt_callback(INTPIN, gpio_callback2, edge='both', pull_up_down=RPIO.PUD_DOWN, debounce_timeout_ms=10)

#Interrupt adatto ad avere un tic ogni 100 msec.
#RPIO.add_interrupt_callback(INTPIN, gpio_callback1, edge='rising', pull_up_down=RPIO.PUD_OFF, debounce_timeout_ms=100)
#Interrupt adatto ad avere un tic ogni 2,87 msec. il massimo che si ottiene con le resistenze scelte
RPIO.add_interrupt_callback(INTPIN, gpio_callback1, edge='rising', pull_up_down=RPIO.PUD_OFF)#, debounce_timeout_ms=100)

# Starts waiting for interrupts (exit with Ctrl+C)
# RPIO.wait_for_interrupts()   # blocks until interrupt, never proceeds beyond this point

RPIO.wait_for_interrupts(threaded=True)   # non-blocking, separate thread

while (1):
   now = datetime.datetime.now()
   dstr = str(now.strftime("%Y-%m-%d_%H:%M:%S"))
   if (dCount > 0):
      dAvg = dSum / dCount
   print("Time: %s Avg: %08.6f Min: %08.6f Max: %08.6f Total: %d" % (dstr, dAvg, dMin, dMax, dCount))
   time.sleep(1)  #10) Stampa 1 volta ogni secondo 

