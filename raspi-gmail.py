#!/usr/bin/env python
 
import RPi.GPIO as GPIO, feedparser, time
 
#DEBUG = 1
# 
#USERNAME = "belcocco" # just the part before the @ sign, add yours here
#PASSWORD = "xpaiqalq"
# 
#NEWMAIL_OFFSET = 1 # my unread messages never goes to zero, yours might
#MAIL_CHECK_FREQ = 60 # check mail every 60 seconds
# 
#GPIO.setmode(GPIO.BCM)
#GREEN_LED = 7
#RED_LED = 8
#GPIO.setup(GREEN_LED, GPIO.OUT)
#GPIO.setup(RED_LED, GPIO.OUT)
# 
#while True:
# 
#newmails = int(feedparser.parse("https://" + USERNAME + ":" + PASSWORD +"@mail.google.com/gmail/feed/atom")["feed"]["fullcount"])
# 
#if DEBUG:
#print "You have", newmails, "new emails!"
# 
#if newmails > NEWMAIL_OFFSET:
#GPIO.output(GREEN_LED, True)
#GPIO.output(RED_LED, False)
#else:
#GPIO.output(GREEN_LED, False)
#GPIO.output(RED_LED, True)
# 
#time.sleep(MAIL_CHECK_FREQ)
#####################################################################

import RPi.GPIO as GPIO, feedparser
USERNAME="belcocco@gmail.com"
PASSWORD="xpaiqalq"
GPIO_PIN=7
GPIO.setmode(GPIO.BOARD)
GPIO.setup(GPIO_PIN, GPIO.OUT)
newmails = int(feedparser.parse("https://" + USERNAME + ":" + PASSWORD + "@mail.google.com/gmail/feed/atom")["feed"]["fullcount"])
if newmails > 0:
	GPIO.output(GPIO_PIN, True)
else:
	GPIO.output(GPIO_PIN, False)
