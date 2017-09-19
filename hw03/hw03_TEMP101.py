#!/usr/bin/env python3

############################################
# HW03_TEMP101.py
# Reads and alerts from TMP101 sensors created by Ryan Evans.
# Run with python3 HW03_TMP101.py
# September 19, 2017
############################################


# Read a TMP101 sensor
# sudo apt install python3-smbus

import smbus
import time
import Adafruit_BBIO.GPIO as GPIO

#Buttons are the Alert pins of the TMP101 sensors
Buttons = ["GP0_3","GP0_4","GP0_5","GP0_6"];

for Button in Buttons:
    GPIO.setup(Button, GPIO.IN)
time.sleep(.01);

#Bus Number
bus = smbus.SMBus(1)
address1 = 0x48
address2 = 0x49
config = bus.read_byte_data(address1,1)
newConfig = config^0x45
bus.write_byte_data(address1,1,0b01100100)  #12 bit accuracy, active high
bus.write_word_data(address1,2,0x0021)      #33 of above for Thigh
bus.write_word_data(address1,3,0x0020)      #32 or below for Tlow

bus.write_byte_data(address2,1,0b01100100)  #12 bit accuracy, active high
bus.write_word_data(address2,2,0x0021)      #33 of above for Thigh
bus.write_word_data(address2,3,0x0020)      #32 or below for Tlow
time.sleep(1)


while True:
    temp1 = bus.read_byte_data(address1,0)
    temp2 = bus.read_byte_data(address2,0)
    #If either sensor is alerting, print alert statement
    if (GPIO.input(Buttons[0])|GPIO.input(Buttons[1])):
        print ("!!Alarm!!: " + str(temp1) + " " + str(temp2), end="\n")
    else:
        print ("No  Alarm: " + str(temp1) + " " + str(temp2), end="\n")
    time.sleep(.25); #Allow other proccess to run

GPIO.cleanup();