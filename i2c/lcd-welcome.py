#!/usr/bin/env python
# -*- coding: latin-1 *-*
# -*- coding: cp1252 -*-
# Raspberry Pi
#
# Python-SMBus and LCD-Display 20x4 (HD44780)
#
# Dic 2013

# I2C address of LCD-Display HD44780 is: 0x27
from ast import literal_eval
import lcddriver1
from subprocess import *
import time

lcd = lcddriver1.lcd()

#lcd.lcd_display_string("AAAAAAAAAAAAAAAAAAAA", 1)
#lcd.lcd_display_string("BBBBBBBBBBBBBBBBBBBB", 2)
#lcd.lcd_display_string("CCCCCCCCCCCCCCCCCCCC", 3)
#lcd.lcd_display_string("DDDDDDDDDDDDDDDDDDDD", 4)
 
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
base_dir = '/sys/class/i2c-adapter/i2c-1/1-0068/rtc/rtc0'
RTC_date_file = base_dir + '/date'
RTC_time_file = base_dir + '/time'

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

try:
        ip_addr = run_cmd(cmd)
        ip_addr = "  IP: " + ip_addr.rstrip("\n") + "   "
        print ip_addr                
        lcd.lcd_display_string(ip_addr, 2)      #display ip address on line 2

        while True:
                date_raw = read_date_raw()
                time_raw = read_time_raw()
                date_pure = date_raw[0]
                time_pure = time_raw[0]
                date_time = date_pure.strip("\n") + "  " + time_pure.strip("\n")
                print date_time
                lcd.lcd_display_string(date_time, 1)
                time.sleep(1)

except KeyboardInterrupt:
        print " "
        print "Ciao !"
#        RPIO.cleanup()
#RPIO.cleanup()


