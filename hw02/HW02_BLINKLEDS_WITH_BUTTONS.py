#!/usr/bin/env python3
import Adafruit_BBIO.GPIO as GPIO
import time

#LEDs = ["USR0","USR1","USR2","USR3"];
LEDs = ["GP1_3","GP1_4","RED","GREEN"];
Buttons = ["GP0_3","GP0_4","GP0_5","GP0_6"];
map = {Buttons[0]:LEDs[0], Buttons[1]:LEDs[1], Buttons[2]:LEDs[2], Buttons[3]:LEDs[3]}

def updateLED(channel):
    print("channel = " + channel);
    state = GPIO.input(channel);
    GPIO.output(map[channel], state);
    print(map[channel] + " Toggled");
    

delay = 0.1;
#Setup LEDs
for LED in LEDs:
    GPIO.setup(LED, GPIO.OUT)   #Setup LED for output

time.sleep(.05);
####Setup Buttons
for Button in Buttons:
    #GPIO.setup(Button, GPIO.OUT)
    GPIO.setup(Button, GPIO.IN)
    GPIO.add_event_detect(Button, GPIO.BOTH, callback=updateLED) #Add event to Button
time.sleep(.05);



    
print("Running");

try:
    while True:
        time.sleep(100); #Allow other proccess to run
except KeyboardInterrupt:
    print("Cleaning Up");
    GPIO.cleanup();
GPIO.cleanup();
