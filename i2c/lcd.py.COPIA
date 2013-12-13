#!/usr/bin/env python
#
# Basic example of using Python-SMBus and a display HD44780
#
#  Display a string of 80 characters
#
# Dic 2013

# I2C address of Display HD44780 is: 0x27

import lcddriver1
from time import *

lcd = lcddriver1.lcd()

#lcd.lcd_display_string("AAAAAAAAAAAAAAAAAAAACCCCCCCCCCCCCCCCCCCCBBBBBBBBBBBBBBBBBBBBDDDDDDDDDDDDDDDDDDDD", 1)
 
lcd.lcd_display_string("*** Hello world ***", 1)
lcd.lcd_display_string("My name is Raspi :-)", 2)
lcd.lcd_display_string("*******************", 3)
lcd.lcd_display_string("***** The Best *****", 4)
