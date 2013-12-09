#!/usr/bin/env python
#
# Basic example of using Python-SMBus and a display HD44780
#
#  Display a string of 80 characters
#
# Dic 2013

# I2C address of Display HD44780 is: 0x27

import lcddriver
from time import *

lcd = lcddriver.lcd()

lcd.lcd_display_string("AAAAAAAAAAAAAAAAAAAACCCCCCCCCCCCCCCCCCCCBBBBBBBBBBBBBBBBBBBBDDDDDDDDDDDDDDDDDDDD", 1)

