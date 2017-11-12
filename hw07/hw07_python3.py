#!/usr/bin/env python3
import Adafruit_BBIO.GPIO as GPIO
import time

map = {"GP1_3":"RED"}

def updateLED(channel):
    GPIO.output(map[channel], GPIO.input(channel));
    

delay = 0.1;
GPIO.setup("RED", GPIO.OUT)   #Setup LED for output

time.sleep(.05);
GPIO.setup("GP1_3", GPIO.IN)
GPIO.add_event_detect("GP1_3", GPIO.BOTH, callback=updateLED) #Add event to Button
time.sleep(.05);

print("Running");

try:
    while True:
        time.sleep(1); #Allow other proccess to run
        
except KeyboardInterrupt:
    print("Cleaning Up");
    GPIO.cleanup();
GPIO.cleanup();
