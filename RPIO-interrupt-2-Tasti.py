#!/usr/bin/env python
# -*- coding: latin-1 *-*
# -*- coding: cp1252 -*-
# Raspberry Pi - GPIO interface with RPIO Interrupt Python module
# RPIO Documentation: http://pythonhosted.org/RPIO
import RPIO, time, datetime

################################ INIZIALIZZAZIONI
INTtasto1 = 24      # define GPIO number for interrupt tasto 1
INTtasto2 = 23      # define GPIO number for interrupt tasto 2
led1=7      # define GPIO number for output Led 1
led2=8      # define GPIO number for output Led 2
led3=25      # define GPIO number for output Led 3

lastTime = time.time()
dMax = 0;
dMin = 2;
dSum = 0;
dCount = 0;
dAvg = 0;
dFirst = 1;

# set up input channels with pull-up control. Can be PUD_UP, PUD_DOWN or PUD_OFF (default)
RPIO.setup(INTtasto1, RPIO.IN, pull_up_down=RPIO.PUD_UP)
RPIO.setup(INTtasto2, RPIO.IN, pull_up_down=RPIO.PUD_UP)
# set up output channels
RPIO.setup(led1, RPIO.OUT)
RPIO.setup(led2, RPIO.OUT)
RPIO.setup(led3, RPIO.OUT)

# read input from gpio
input_value_t1 = RPIO.input(INTtasto1)
input_value_t2 = RPIO.input(INTtasto2)

# state - decides what LED should be on and off
state = 0

# increment - the direction of states
inc = 1

#ISR alla pressione del tasto 1
def gpio_callback1(gpio_id, val):
	global inc, state, lastTime, dMax, dMin, dSum, dCount, dFirst
	if (inc == 1):
		state = state + 1;
	else:
		state = state - 1;

	# reached the max state, time to go back (decrement)
	if (state == 3):
		inc = 0
	# reached the min state, go back up (increment)
	elif (state == 0):
		inc = 1

	if (state == 1):
		RPIO.output(led1, RPIO.HIGH)
		RPIO.output(led2, RPIO.LOW)
		RPIO.output(led3, RPIO.LOW)
	elif (state == 2):
		RPIO.output(led1, RPIO.HIGH)
		RPIO.output(led2, RPIO.HIGH)
		RPIO.output(led3, RPIO.LOW)
	elif (state == 3):
		RPIO.output(led1, RPIO.HIGH)
		RPIO.output(led2, RPIO.HIGH)
		RPIO.output(led3, RPIO.HIGH)
	else:
		RPIO.output(led1, RPIO.LOW)
		RPIO.output(led2, RPIO.LOW)
		RPIO.output(led3, RPIO.LOW)
	print("Tasto 1 Premuto", state)

#ISR alla pressione del tasto 2 di Reset
def gpio_callback2(gpio_id, val):
	global inc, state, lastTime, dMax, dMin, dSum, dCount, dFirst

	state = 0
	inc = 1
	RPIO.output(led1, RPIO.LOW)
	RPIO.output(led2, RPIO.LOW)
	RPIO.output(led3, RPIO.LOW)

	print("Tasto 2 di Reset premuto", state)


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
#		print("CB1: gpio %s: %s at %s delta: %08.6f" % (gpio_id, val, dstr, dTime))


# GPIO interrupt callbacks. Note this resets any previous config of pullup resistor
# RPIO.add_interrupt_callback(INTPIN, gpio_callback2, edge='falling',pull_up_down=RPIO.PUD_UP, debounce_timeout_ms=100)
# RPIO.add_interrupt_callback(INTPIN, gpio_callback2, edge='both', pull_up_down=RPIO.PUD_DOWN, debounce_timeout_ms=10)

#Interrupt adatto ad avere un tic ogni 100 msec.
#RPIO.add_interrupt_callback(INTPIN, gpio_callback1, edge='rising', pull_up_down=RPIO.PUD_OFF, debounce_timeout_ms=100)
#Interrupt adatto ad avere un tic ogni 2,87 msec. il massimo che si ottiene con le resistenze scelte
RPIO.add_interrupt_callback(INTtasto1, gpio_callback1, edge='rising', pull_up_down=RPIO.PUD_OFF)#, debounce_timeout_ms=100)
RPIO.add_interrupt_callback(INTtasto2, gpio_callback2, edge='rising', pull_up_down=RPIO.PUD_OFF)#, debounce_timeout_ms=100)

# Starts waiting for interrupts (exit with Ctrl+C)
# RPIO.wait_for_interrupts()   # blocks until interrupt, never proceeds beyond this point

RPIO.wait_for_interrupts(threaded=True)   # non-blocking, separate thread

#Loop principale che non fa niente. Aspetta e basta.
try:
	while (1):
   		time.sleep(1)  #aspetta 

except KeyboardInterrupt:
        print " "
        print "Ciao !"
        RPIO.cleanup()
RPIO.cleanup()


