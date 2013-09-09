#!/usr/bin/env python
#Raspberry Pi - GPIO Interface
#Check if exist new mail on gmail.com 
#Use one led or two leds output
#Comment code that is not used
 
import RPi.GPIO as GPIO, feedparser
from time import sleep


###############
#Two Leds used# 
###############
DEBUG = 1
 
USERNAME = "belcocco@gmail.com" # just the part before the @ sign, add yours here
PASSWORD = "xpaiqalq"
 
NEWMAIL_OFFSET = 1 # my unread messages never goes to zero, yours might
#MAIL_CHECK_FREQ = 60 # check mail every 60 seconds
MAIL_CHECK_FREQ = 1800 # check mail every 30 minutes
 
GPIO.setmode(GPIO.BCM)
GREEN_LED = 11
RED_LED = 8
GPIO.setup(GREEN_LED, GPIO.OUT)
GPIO.setup(RED_LED, GPIO.OUT)
 
while True:
 
	newmails = int(feedparser.parse("https://" + USERNAME + ":" + PASSWORD +"@mail.google.com/gmail/feed/atom")["feed"]["fullcount"])
 
	if DEBUG:
		print "You have", newmails, "new emails!"
 
	if newmails >= NEWMAIL_OFFSET:
		GPIO.output(GREEN_LED, True)
		GPIO.output(RED_LED, False)
	else:
		GPIO.output(GREEN_LED, False)
		GPIO.output(RED_LED, True)
 
	sleep(MAIL_CHECK_FREQ)


##############
#One led used#
##############
#USERNAME="belcocco@gmail.com"
#PASSWORD="xpaiqalq"
#
#GPIO_channel=8
#GPIO.setmode(GPIO.BCM)
#GPIO.setup(GPIO_channel, GPIO.OUT)
#newmails = int(feedparser.parse("https://" + USERNAME + ":" + PASSWORD + "@mail.google.com/gmail/feed/atom")["feed"]["fullcount"])
#if newmails > 0:
#	GPIO.output(GPIO_channel, True)
#else:
#	GPIO.output(GPIO_channel, False)

