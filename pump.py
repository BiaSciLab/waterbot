#!/usr/bin/env python

# Import libraries
from __future__ import print_function #for printing
import RPi.GPIO as GPIO, time, os
from PIL import Image #for printing Images
from Adafruit_Thermal import * #printer library

printer = Adafruit_Thermal("/dev/serial0", 19200, timeout=5)

DEBUG = 1

# Pin 'constants'
water_empty = 12
water_full = 16
flow_sensor = 21
relay = 26
PulsesPer_mL = 650 # data sheet says 450 pulses per Liter my testing got 650

#Variables
pulses = 0
ok_to_print = False

#Set Up the Pi
GPIO.setmode(GPIO.BCM)
GPIO.setup(water_empty, GPIO.IN, pull_up_down = GPIO.PUD_DOWN) #12 is the empty sensor
GPIO.setup(water_full,  GPIO.IN, pull_up_down = GPIO.PUD_DOWN) #16 is the full sensor
GPIO.setup(flow_sensor, GPIO.IN, pull_up_down = GPIO.PUD_DOWN) #21 is the flow meter
GPIO.setup(relay, GPIO.OUT) #26 is the relay for the motor

# Functions
def Pulse_Count(Ppin):
    global pulses
    pulses = pulses+1

def PumpOn (Ppin):
    GPIO.output(Ppin, GPIO.HIGH)

def PumpOff (Ppin):
    GPIO.output(Ppin, GPIO.LOW)

# inturrupts
GPIO.add_event_detect(flow_sensor, GPIO.RISING, callback = Pulse_Count) # Counts pulses when they happen

# Main Code
while True:
    # Water Full
    if (GPIO.input(water_full) == True) and (ok_to_print == True): #Full AND ok to print, so it only prints once
        PumpOff (relay) # turn off the pump!
        current_time = time.ctime() # Get the current time and store it
        time.sleep(1)
        mL_despensed = pulses / PulsesPer_mL # converts pulses to mL
        print ("{} mL on ".format(mL_despensed) + current_time) #prints to the screen
        printer.println("{} mL despensed on ".format(mL_despensed)) #prints to the printer
        printer.println(current_time)
        printer.feed(1)
        printer.printImage(Image.open('BiaBotLabLogoPrint.png'), True)
        printer.feed(1)
        printer.println("Follow me on Twitter:")
        printer.println("@BiaSciLab")
        printer.feed(3)
        ok_to_print = False # sets it not print again until next time
        pulses = 0 # resets pulses
        time.sleep(15) # waits for it to finish printing

    # Water Empty
    if (GPIO.input(water_empty) == True) or (GPIO.input(water_full) == False):
        PumpOn (relay) # turns on the pump 
        mL_despensed = pulses / PulsesPer_mL # counts pulses while it fills
        print ("{} mL".format(mL_despensed)) # prints pulses to the screen
        ok_to_print = True # Tells the printer it can print when its done filling
        time.sleep(.001)
