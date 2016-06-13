#! /usr/bin/env python
"""PiSkate a python script which uses the Raspberry Pi 3 to control an ESC via a Bluetooth
Wii Remote.

Requires the RPi library and cwiid library

Copyright (C) 2016 Tim Maier. Free use of this software is
granted under the terms of Creative Commons Attribution-ShareAlike 4.0 International License:
http://creativecommons.org/licenses/by-sa/4.0/."""

import RPi.GPIO as GPIO
import cwiid
import time 

#
# Constants
#
SERVO = 2 # GPIO number of servo control
PERIOD = 20 # Time in ms for one period
STOP = 5 # 5 is absolute min
MAX = 9.7 # 10 is absolute max
INC = 0.1
BUTTON_PLUS = 2048
BUTTON_MINUS = 1024
BUTTON_B = 4
BUTTON_HOME = 128


#
# Init GPIO
#
GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO, GPIO.OUT)

#
# Init Wii Mote and loop till connected
#
while True:
   try:
      wm = cwiid.Wiimote()
      break
   except:
      pass
wm.rpt_mode = cwiid.RPT_BTN # Enable button data reporting

#
# Setup ESC limits
#
servo = GPIO.PWM(SERVO, 1000 / PERIOD)
servo.start(10)
servo.ChangeDutyCycle(5)
#
# Userloop
#
print ('increase > Up+B | decrease > Down+B | quit > HOME')

dc = STOP
cycling = True
try:
    while cycling:
        servo.ChangeDutyCycle(dc)
        res = wm.state['buttons']
        print res, dc
        if res & (BUTTON_PLUS | BUTTON_B) == BUTTON_PLUS+BUTTON_B: 
            dc = dc + INC
        if res & (BUTTON_MINUS | BUTTON_B) == BUTTON_MINUS+BUTTON_B:
            dc = dc - INC
        if res & BUTTON_B == 0: #B = dead switch is be active or not
            dc = STOP 
        if res == BUTTON_HOME:
            cycling = False
        if dc > MAX:
            dc = MAX
        if dc < STOP:
            dc = STOP
        time.sleep(0.1)
finally:
    # shut down cleanly
    servo.stop()
    print ("dc var setting is: ")
    print (dc)

#
# Shutdown/cleanup
#
servo.stop()
GPIO.cleanup()
