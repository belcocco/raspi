#!/usr/bin/env python
# -*- coding: latin-1 *-*
# -*- coding: cp1252 -*-
# 
# Raspberry Pi - GPIO interface with RPIO Interrupt Python module
# P1 header 2-26: 5V0 5V0 GND  14  15  18  GND  23  24   GND  25  08  07
# P1 header 1-25: 3V3  02  03  04  GND 17  27   22  3V3  10   09  11  GND

# DISCAR Device
# Usa INT11, INT9, INT10, INT22 per gestire i tasti riga 1, 2, 3, 4 del display LCD  


import RPIO, time, datetime
from i2c import I2C
import smbus

from ast import literal_eval
import lcddriver1
from subprocess import *


#import welcome

#------------------INIZIALIZZAZIONI
#Canali su pin PARI
#INT7 = 7      # define GPIO number 7 for interrupt from IC
#INT8 = 8      # define GPIO number 8 for interrupt from IC
#INT25 = 25      # define GPIO number 25 for interrupt from IC
#INT24 = 24      # define GPIO number 24 for interrupt from IC
#INT23 = 23      # define GPIO number 23 for interrupt from IC
#INT18 = 18      # define GPIO number 18 for interrupt from IC (PWM)

#Canali su pin DISPARI
INT11 = 11      # GPIO 11 interrupt tasto rosso = riga 1 display LCD 
INT9 = 9        # GPIO 9 interrupt tasto nero = riga 2 display LCD
INT10 = 10      # GPIO 10 interrupt tasto nero = riga 3 display LCD
INT22 = 22      # GPIO 22 interrupt tasto nero = riga 4 display LCD
#INT27 = 27      # define GPIO number 27 for interrupt from IC
#INT17 = 17      # define GPIO number 17 for interrupt from IC

#Canali per UART
#INT14 = 14      # define GPIO number 14 for interrupt from IC (UART Tx)
#INT15 = 15      # define GPIO number 15 for interrupt from IC (UART Rx)

MCP23017_IODIRA = 0x00
MCP23017_IODIRB = 0x01
MCP23017_GPIOA  = 0x12
MCP23017_GPIOB  = 0x13
MCP23017_GPPUA  = 0x0C
MCP23017_GPPUB  = 0x0D
MCP23017_OLATA  = 0x14
MCP23017_OLATB  = 0x15
MCP23008_GPIOA  = 0x09
MCP23008_GPPUA  = 0x06
MCP23008_OLATA  = 0x0A


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

dMax3 = 0;
dMin3 = 2;
dSum3 = 0;
dCount3 = 0;
dAvg3 = 0;
dFirst3 = 1;

dMax4 = 0;
dMin4 = 2;
dSum4 = 0;
dCount4 = 0;
dAvg4 = 0;
dFirst4 = 1;

# set up input channel with pull-up control. Can be PUD_UP, PUD_DOWN or PUD_OFF (default)
#Tutti i canali sono settati in ingresso, quando serve  settare l'output da programma
#RPIO.setup(INT7, RPIO.IN, pull_up_down=RPIO.PUD_UP)
#RPIO.setup(INT8, RPIO.IN, pull_up_down=RPIO.PUD_UP)
#RPIO.setup(INT25, RPIO.IN, pull_up_down=RPIO.PUD_UP)
#RPIO.setup(INT24, RPIO.IN, pull_up_down=RPIO.PUD_UP)
#RPIO.setup(INT23, RPIO.IN, pull_up_down=RPIO.PUD_UP)
#RPIO.setup(INT18, RPIO.IN, pull_up_down=RPIO.PUD_UP)
RPIO.setup(INT11, RPIO.IN, pull_up_down=RPIO.PUD_UP)
RPIO.setup(INT9, RPIO.IN, pull_up_down=RPIO.PUD_UP)
RPIO.setup(INT10, RPIO.IN, pull_up_down=RPIO.PUD_UP)
RPIO.setup(INT22, RPIO.IN, pull_up_down=RPIO.PUD_UP)
#RPIO.setup(INT27, RPIO.IN, pull_up_down=RPIO.PUD_UP)
#RPIO.setup(INT17, RPIO.IN, pull_up_down=RPIO.PUD_UP)
#RPIO.setup(INT14, RPIO.IN, pull_up_down=RPIO.PUD_UP)
#RPIO.setup(INT15, RPIO.IN, pull_up_down=RPIO.PUD_UP)

# read all input from gpio
#input_value_7 = RPIO.input(INT7)
#input_value_8 = RPIO.input(INT8)
#input_value_25 = RPIO.input(INT25)
#input_value_24 = RPIO.input(INT24)
#input_value_23 = RPIO.input(INT23)
#input_value_18 = RPIO.input(INT18)
input_value_11 = RPIO.input(INT11)
input_value_9 = RPIO.input(INT9)
input_value_10 = RPIO.input(INT10)
input_value_22 = RPIO.input(INT22)
#input_value_27 = RPIO.input(INT27)
#input_value_17 = RPIO.input(INT17)
#input_value_14 = RPIO.input(INT14)
#input_value_15 = RPIO.input(INT15)

class MCP230XX(object):
    OUTPUT = 0
    INPUT = 1

    def __init__(self, address, num_gpios):
        assert num_gpios >= 0 and num_gpios <= 16, "Number of GPIOs must be between 0 and 16"
        self.i2c = I2C(address=address)
        self.address = address
        self.num_gpios = num_gpios

        # set defaults
        if num_gpios <= 8:
            self.i2c.write8(MCP23017_IODIRA, 0xFF)  # all inputs on port A
            self.direction = self.i2c.readU8(MCP23017_IODIRA)
            self.i2c.write8(MCP23008_GPPUA, 0x00)
        elif num_gpios > 8 and num_gpios <= 16:
            self.i2c.write8(MCP23017_IODIRA, 0x00)  # GPA0-7 all OUTPUTS (with 0xFF all inputs on port A)
            self.i2c.write8(MCP23017_IODIRB, 0x00)  # GPB0-7 all OUTPUTS (with 0xFF all inputs on port B)
            self.direction = self.i2c.readU8(MCP23017_IODIRA)
            self.direction |= self.i2c.readU8(MCP23017_IODIRB) << 8
            self.i2c.write8(MCP23017_GPPUA, 0x00)
            self.i2c.write8(MCP23017_GPPUB, 0x00)

    def _changebit(self, bitmap, bit, value):
        assert value == 1 or value == 0, "Value is %s must be 1 or 0" % value
        if value == 0:
            return bitmap & ~(1 << bit)
        elif value == 1:
            return bitmap | (1 << bit)

    def _readandchangepin(self, port, pin, value, currvalue = None):
        assert pin >= 0 and pin < self.num_gpios, "Pin number %s is invalid, only 0-%s are valid" % (pin, self.num_gpios)
        #assert self.direction & (1 << pin) == 0, "Pin %s not set to output" % pin
        if not currvalue:
             currvalue = self.i2c.readU8(port)
        newvalue = self._changebit(currvalue, pin, value)
        self.i2c.write8(port, newvalue)
        return newvalue

    def pullup(self, pin, value):
        if self.num_gpios <= 8:
            return self._readandchangepin(MCP23008_GPPUA, pin, value)
        if self.num_gpios <= 16:
            lvalue = self._readandchangepin(MCP23017_GPPUA, pin, value)
            if (pin < 8):
                return
            else:
                return self._readandchangepin(MCP23017_GPPUB, pin-8, value) << 8

    # Set pin to either input or output mode
    def config(self, pin, mode):
        if self.num_gpios <= 8:
            self.direction = self._readandchangepin(MCP23017_IODIRA, pin, mode)
        if self.num_gpios <= 16:
            if (pin < 8):
                self.direction = self._readandchangepin(MCP23017_IODIRA, pin, mode)
            else:
                self.direction |= self._readandchangepin(MCP23017_IODIRB, pin-8, mode) << 8

        return self.direction

    def output(self, pin, value):
        # assert self.direction & (1 << pin) == 0, "Pin %s not set to output" % pin
        if self.num_gpios <= 8:
            self.outputvalue = self._readandchangepin(MCP23008_GPIOA, pin, value, self.i2c.readU8(MCP23008_OLATA))
        if self.num_gpios <= 16:
            if (pin < 8):
                self.outputvalue = self._readandchangepin(MCP23017_GPIOA, pin, value, self.i2c.readU8(MCP23017_OLATA))
            else:
                self.outputvalue = self._readandchangepin(MCP23017_GPIOB, pin-8, value, self.i2c.readU8(MCP23017_OLATB)) << 8

        return self.outputvalue


        self.outputvalue = self._readandchangepin(MCP23017_IODIRA, pin, value, self.outputvalue)
        return self.outputvalue

    def input(self, pin):
        assert pin >= 0 and pin < self.num_gpios, "Pin number %s is invalid, only 0-%s are valid" % (pin, self.num_gpios)
        assert self.direction & (1 << pin) != 0, "Pin %s not set to input" % pin
        if self.num_gpios <= 8:
            value = self.i2c.readU8(MCP23008_GPIOA)
        elif self.num_gpios > 8 and self.num_gpios <= 16:
            value = self.i2c.readU8(MCP23017_GPIOA)
            value |= self.i2c.readU8(MCP23017_GPIOB) << 8
        return value & (1 << pin)

    def readU8(self):
        result = self.i2c.readU8(MCP23008_OLATA)
        return(result)

    def readS8(self):
        result = self.i2c.readU8(MCP23008_OLATA)
        if (result > 127): result -= 256
        return result

    def readU16(self):
        assert self.num_gpios >= 16, "16bits required"
        lo = self.i2c.readU8(MCP23017_OLATA)
        hi = self.i2c.readU8(MCP23017_OLATB)
        return((hi << 8) | lo)

    def readS16(self):
        assert self.num_gpios >= 16, "16bits required"
        lo = self.i2c.readU8(MCP23017_OLATA)
        hi = self.i2c.readU8(MCP23017_OLATB)
        if (hi > 127): hi -= 256
        return((hi << 8) | lo)

    def write8(self, value):
        self.i2c.write8(MCP23008_OLATA, value)

    def write16(self, value):
        assert self.num_gpios >= 16, "16bits required"
        self.i2c.write8(MCP23017_OLATA, value & 0xFF)
        self.i2c.write8(MCP23017_OLATB, (value >> 8) & 0xFF)
# RPi.GPIO compatible interface for MCP23017 and MCP23008

class MCP230XX_GPIO(object):
    OUT = 0
    IN = 1
    BCM = 0
    BOARD = 0
    def __init__(self, busnum, address, num_gpios):
        self.chip = MCP230XX(busnum, address, num_gpios)
    def setmode(self, mode):
        # do nothing
        pass
    def setup(self, pin, mode):
        self.chip.config(pin, mode)
    def input(self, pin):
        return self.chip.input(pin)
    def output(self, pin, value):
        self.chip.output(pin, value)
    def pullup(self, pin, value):
        self.chip.pullup(pin, value)

#Definizione della callback per impulsi da GPIO 11
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
      #stampa ogni tic generato da PWM canale-dma-0 GPIO-25  
#      print("PWM--->gpio %s: %s at %s delta: %08.6f" % (gpio_id, val, dstr1, dTime1))

#Definizione della callback per impulsi da GPIO 9
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
      #stampa ogni tic generato da PWM canale-dma-2 GPIO-24
#      print("PWM--->gpio %s: %s at %s delta: %08.6f" % (gpio_id, val, dstr2, dTime2))

#Definizione della callback per impulsi da GPIO 10
def gpio_callback_INT10(gpio_id, val):
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
      #stampa ogni tic generato da PWM canale-dma-3 GPIO-23
#      print("PWM--->gpio %s: %s at %s delta: %08.6f" % (gpio_id, val, dstr3, dTime3))

#Definizione della callback per impulsi da GPIO 22
def gpio_callback_INT22(gpio_id, val):
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
      #stampa ogni tic generato da PWM canale-dma-3 GPIO-18
#      print("PWM--->gpio %s: %s at %s delta: %08.6f" % (gpio_id, val, dstr4, dTime4))

# GPIO interrupt callbacks. Note this resets any previous config of pullup resistor
# RPIO.add_interrupt_callback(INTPIN, gpio_callback2, edge='falling',pull_up_down=RPIO.PUD_UP, debounce_timeout_ms=100)
# RPIO.add_interrupt_callback(INTPIN, gpio_callback2, edge='both', pull_up_down=RPIO.PUD_DOWN, debounce_timeout_ms=10)

#Interrupt adatto ad avere un tic ogni 100 msec.
#RPIO.add_interrupt_callback(INTPIN, gpio_callback1, edge='rising', pull_up_down=RPIO.PUD_OFF, debounce_timeout_ms=100)
#Interrupt adatto ad avere un tic ogni 2,87 msec. il massimo che si ottiene con le resistenze scelte
#RPIO.add_interrupt_callback(INT7, gpio_callback_INT7, edge='rising', pull_up_down=RPIO.PUD_UP)#, debounce_timeout_ms=100)
#RPIO.add_interrupt_callback(INT8, gpio_callback_INT8, edge='rising', pull_up_down=RPIO.PUD_UP)#, debounce_timeout_ms=100)
#RPIO.add_interrupt_callback(INT25, gpio_callback_INT25, edge='rising', pull_up_down=RPIO.PUD_UP)#, debounce_timeout_ms=100)
#RPIO.add_interrupt_callback(INT24, gpio_callback_INT24, edge='rising', pull_up_down=RPIO.PUD_UP)#, debounce_timeout_ms=100)
#RPIO.add_interrupt_callback(INT23, gpio_callback_INT23, edge='rising', pull_up_down=RPIO.PUD_UP)#, debounce_timeout_ms=100)
#RPIO.add_interrupt_callback(INT18, gpio_callback_INT18, edge='rising', pull_up_down=RPIO.PUD_UP)#, debounce_timeout_ms=100)
RPIO.add_interrupt_callback(INT11, gpio_callback_INT11, edge='rising', pull_up_down=RPIO.PUD_UP)#, debounce_timeout_ms=100)
RPIO.add_interrupt_callback(INT9, gpio_callback_INT9, edge='rising', pull_up_down=RPIO.PUD_UP)#, debounce_timeout_ms=100)
RPIO.add_interrupt_callback(INT10, gpio_callback_INT10, edge='rising', pull_up_down=RPIO.PUD_UP)#, debounce_timeout_ms=100)
RPIO.add_interrupt_callback(INT22, gpio_callback_INT22, edge='rising', pull_up_down=RPIO.PUD_UP)#, debounce_timeout_ms=100)
#RPIO.add_interrupt_callback(INT27, gpio_callback_INT27, edge='rising', pull_up_down=RPIO.PUD_UP)#, debounce_timeout_ms=100)
#RPIO.add_interrupt_callback(INT17, gpio_callback_INT17, edge='rising', pull_up_down=RPIO.PUD_UP)#, debounce_timeout_ms=100)
#RPIO.add_interrupt_callback(INT14, gpio_callback_INT14, edge='rising', pull_up_down=RPIO.PUD_UP)#, debounce_timeout_ms=100)
#RPIO.add_interrupt_callback(INT15, gpio_callback_INT15, edge='rising', pull_up_down=RPIO.PUD_UP)#, debounce_timeout_ms=100)

# Starts waiting for interrupts (exit with Ctrl+C)
# RPIO.wait_for_interrupts()   # blocks until interrupt, never proceeds beyond this point

RPIO.wait_for_interrupts(threaded=True)   # non-blocking, separate thread


if __name__ == '__main__':
#try:
    import welcome
 
    # ***************************************************
    # Set num_gpios to 8 for MCP23008 or 16 for MCP23017!
    # ***************************************************
    #mcp = MCP230XX(address = 0x20, num_gpios = 8) # MCP23008 e MCP23017 hanno Ind. Base 20H
    mcp = MCP230XX(address = 0x22, num_gpios = 16) # A0 a massa, A1 a +5V, A2 a massa. Il mio MCP23017 è all'indirizzo 22H


    def run_cmd(cmd):
         p = Popen(cmd, shell=True, stdout=PIPE)
         output = p.communicate()[0]
         return output

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


    # Tutti i pin sono settati come OUTPUT di default.
    # Da programma si può intervenire ad esempio con:
    #mcp.config(0, mcp.OUTPUT)
    #mcp.config(1, mcp.OUTPUT)
    #mcp.config(4, mcp.OUTPUT)
    #mcp.config(15, mcp.OUTPUT)
    # Naturalmente si può cambiare un OUTPUT di default in INPUT
    # Esempio: Set pins 0, 11 and 12 to input with the pullup resistor enabled (you can set pins 1...10 and 13...15 this way)
    #mcp.config(0, mcp.INPUT)
    #mcp.pullup(0, 1)
    #mcp.config(11, mcp.INPUT)
    #mcp.pullup(11, 1)
    #mcp.config(12, mcp.INPUT)
    #mcp.pullup(12, 1)

    # Set pin 7 to input with the pullup resistor enabled
#    mcp.config(7, mcp.INPUT)
#    mcp.pullup(7, 1)

    # Read input pin and display the results
#    print "Pin 7 = %d" % (mcp.input(7) >> 7)

    # Python speed test on output 0 toggling at max speed
#    print "Starting blinky on pin 0...6 (CTRL+C to quit)"
    print "Starting blinky on pin 0...15 of MCP23017 expander (CTRL+C to quit)"

    cmd = "ip addr show eth0 | grep inet | awk '{print $2}' | cut -d/ -f1"
    ip_addr = run_cmd(cmd)
    ip_addr = "  IP: " + ip_addr.rstrip("\n") + "   "
    print ip_addr
    lcd.lcd_display_string(ip_addr, 2)      #display ip address on line 2
    lcd.lcd_display_string("  Premi Tasto Rosso ", 4)

#    try:
    while (True):

#        date_raw = read_date_raw()     #read date (as List from file)
#        time_raw = read_time_raw()     #read time (as List from file)
#        RTC_date = os.system('date')
#        print RTC_date
#        date_pure = date_raw[0]
#        time_pure = time_raw[0]
#        date_time = RTC_date
            today_raw = datetime.datetime.now()
            today_pure = today_raw.strftime(" %y-%m-%Y   %H:%M")
            temp_c_raw = read_temp()        #read temp (as float from file)
            temp_c_ = repr(temp_c_raw)       #convert to string
            temp_c_pure = "   Temp. " + temp_c_[:4] + " C"           #only one decimal
# DEBUG         print date_time, "Temp.:",temp_c_pure
                #Visualizza data e ora
            lcd.lcd_display_string(today_pure, 1)
#        lcd.lcd_display_string(RTC_date[:20], 1)
            lcd.lcd_display_string(temp_c_pure , 3)

            time.sleep(.1)

            mcp.output(0, 1)  # Pin 0 High
            time.sleep(.05);
#        mcp.output(1, 1)  # Pin 1 High
#        time.sleep(.05);
#        mcp.output(2, 1)  # Pin 2 High
#        time.sleep(.05);
#        mcp.output(3, 1)  # Pin 3 High
#        time.sleep(.05);
#        mcp.output(4, 1)  # Pin 4 High
#        time.sleep(.05);
#        mcp.output(5, 1)  # Pin 5 High
#        time.sleep(.05);
#        mcp.output(6, 1)  # Pin 6 High
#        time.sleep(.05);
#        mcp.output(7, 1)  # Pin 7 High
#        time.sleep(.05);
#        mcp.output(8, 1)  # Pin 8 High
#        time.sleep(.1);
#        mcp.output(9, 1)  # Pin 9 High
#        time.sleep(.1);
#        mcp.output(10, 1)  # Pin 10 High
#        time.sleep(.1);
#        mcp.output(11, 1)  # Pin 11 High
#        time.sleep(.1);
#        mcp.output(12, 1)  # Pin 12 High
#        time.sleep(.1);
#        mcp.output(13, 1)  # Pin 13 High
#        time.sleep(.1);
#        mcp.output(14, 1)  # Pin 14 High
#        time.sleep(.1);
#        mcp.output(15, 1)  # Pin 15 High
#        time.sleep(.1);

            mcp.output(0, 0)  # Pin 0 Low
            time.sleep(.05);
#        mcp.output(1, 0)  # Pin 1 Low
#        time.sleep(.05);
#        mcp.output(2, 0)  # Pin 2 Low
#        time.sleep(.05);
#        mcp.output(3, 0)  # Pin 3 Low
#        time.sleep(.05);
#        mcp.output(4, 0)  # Pin 4 Low
#        time.sleep(.05);
#        mcp.output(5, 0)  # Pin 5 Low
#        time.sleep(.05);
#        mcp.output(6, 0)  # Pin 6 Low
#        time.sleep(.05);
#        mcp.output(7, 0)  # Pin 7 Low
#        time.sleep(.05);
#        mcp.output(8, 0)  # Pin 8 Low
#        time.sleep(.1);
#        mcp.output(9, 0)  # Pin 9 Low
#        time.sleep(.1);
#        mcp.output(10, 0)  # Pin 10 Low
#        time.sleep(.1);
#        mcp.output(11, 0)  # Pin 11 Low
#        time.sleep(.1);
#        mcp.output(12, 0)  # Pin 12 Low
#        time.sleep(.1);
#        mcp.output(13, 0)  # Pin 13 Low
#        time.sleep(.1);
#        mcp.output(14, 0)  # Pin 14 Low
#        time.sleep(.1);
#        mcp.output(15, 0)  # Pin 15 Low
#        time.sleep(.1);

            now1 = datetime.datetime.now()
            dstr1 = str(now1.strftime("%Y-%m-%d_%H:%M:%S"))
            if (dCount1 > 0):
                dAvg1 = dSum1 / dCount1
            print("Riga 1 - Tasto Rosso Tic Totali: %d" % (dCount1))

            now2 = datetime.datetime.now()
            dstr2 = str(now2.strftime("%Y-%m-%d_%H:%M:%S"))
            if (dCount2 > 0):
                dAvg2 = dSum2 / dCount2
            print("Riga 2 - Tasto nero Tic Totali: %d" % (dCount2))

            now3 = datetime.datetime.now()
            dstr3 = str(now3.strftime("%Y-%m-%d_%H:%M:%S"))
            if (dCount3 > 0):
                dAvg3 = dSum3 / dCount3
            print("Riga 3 - Tasto nero Tic Totali: %d" % (dCount3))

#        now4 = datetime.datetime.now()
#        dstr4 = str(now4.strftime("%Y-%m-%d_%H:%M:%S"))
#        if (dCount4 > 0):
#            dAvg4 = dSum4 / dCount4
#        print("Riga 4 - Tasto nero Tic Totali: %d" % (dCount4))

#        time.sleep(10)  #con (1) Stampa 1 volta ogni secondo
				#con (10) stampa ogni 10 secondi

#except KeyboardInterrupt:
#    RPIO.setwarnings(False)
#    print " "
#    print "Ciao !"
#    RPIO.cleanup()
#RPIO.cleanup()


