#!/usr/bin/env python3
import Adafruit_BBIO.GPIO as GPIO
import time

GPIO.setup("GREEN", GPIO.IN);

while 1:
    print(GPIO.input("GREEN"));
    time.sleep( .25);