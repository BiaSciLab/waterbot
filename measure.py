#!/usr/bin/env python

# Example for RC timing reading for Raspberry Pi
# are not fast enough!

import RPi.GPIO as GPIO, time, os

DEBUG = 1
GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.IN,pull_up_down=GPIO.PUD_DOWN)

pulses = 0

def pulse_count(channel):
    global pulses
    pulses = pulses+1
    print (pulses)

GPIO.add_event_detect(21, GPIO.RISING, callback=pulse_count)

while True:
    print (pulses)
