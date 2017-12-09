#!/usr/bin/env python

# Example for RC timing reading for Raspberry Pi
# are not fast enough!

import RPi.GPIO as GPIO, time, os

DEBUG = 1
GPIO.setmode(GPIO.BCM)

water_full = 0
water_empty = 0

def PumpOn (Ppin):
    GPIO.setup(Ppin, GPIO.OUT)
    GPIO.output(Ppin, GPIO.HIGH)

def PumpOff (Ppin):
    GPIO.setup(Ppin, GPIO.OUT)
    GPIO.output(Ppin, GPIO.LOW)

def RCtime (RCpin):
    reading = 0
    GPIO.setup(RCpin, GPIO.OUT)
    GPIO.output(RCpin, GPIO.LOW)
    time.sleep(0.1)

    GPIO.setup(RCpin, GPIO.IN)
    # This takes about 1 millisecond per loop cycle
    while (GPIO.input(RCpin) == GPIO.LOW):
        reading += 1
        return reading

while True:
    water_full = RCtime(18)
    if water_full > 100:
        print ("water full" + str(water_full))
        PumpOff (24)
    if water_full < 100:
        print ("water empty")
        pumpOn (24)
    print RCtime(18)     # Read RC timing using pin #18

#    water_empty = RCtime(23)
#    if water_empty > 100:
#        print ("rainbow dogs" + str(water_empty))
#        print ("rainbow bricks")
#    print RCtime(23)     # Read RC timing using pin #18
