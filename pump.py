#!/usr/bin/env python

# Import libraries
import RPi.GPIO as GPIO, time, os
from Adafruit_Thermal import *

printer = Adafruit_Thermal("/def/serial0", 19200, timeout=5)

DEBUG = 1

# Pin 'constants'
water_empty = 12
water_full = 16
flow_sensor = 21
relay = 26
PulsesPer_mL = 650.000 # data sheet says 450 pulses per Liter my testing got 650

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
GPIO.add_event_detect(flow_sensor, GPIO.RISING, callback = Pulse_Count)

# Main Code
while True:
    # Water Full
    if (GPIO.input(water_full) == True) and (ok_to_print == True):
        PumpOff (relay)
        current_time = time.ctime()
        time.sleep(1)
        mL_despensed = pulses / PulsesPer_mL
        print ("{} mL on ".format(mL_despensed) + current_time)
        printer.println("{} mL on ".format(mL_despensed) + current_time)
        printer.feed(1)
        ok_to_print = False
        pulses = 0
        time.sleep(3)
    # Water Empty
    if (GPIO.input(water_empty) == True) or (GPIO.input(water_full) == False):
        mL_despensed = pulses / PulsesPer_mL
        print ("{} mL".format(mL_despensed))
        ok_to_print = True # Tells the printer it can print when its done filling
        PumpOn (relay)
        time.sleep(.001)
