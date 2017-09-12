############################################
# HW02_ETHC_A_SKETCH
# Simple screen drawing program created by Ryan Evans.
# Controls are buttons conencted to GP0 for movement.
# PAUSE clears
# MODE exits
# Has configureable WIDTH and HEIGHT settings.
# Run with python3 HW02_ETCH_A_SKETCH.py
# September 12, 2017
############################################

#!/usr/bin/env python3s
import Adafruit_BBIO.GPIO as GPIO
import time
import curses


Buttons = ["GP0_3","GP0_4","GP0_5","GP0_6","PAUSE","MODE"];
map = {Buttons[0]:"RIGHT", Buttons[1]:"UP", Buttons[2]:"DOWN", Buttons[3]:"LEFT", Buttons[4]:"CLEAR",Buttons[5]:"EXIT"}


WIDTH = 8;			#Number of columns
HEIGHT = 8;		#Number of rows
global x;
x = 0;			    #Cursor x coordinate
global y;
y = HEIGHT;			#Cursor y coordinate
	
stdscr = curses.initscr(); 			#initialize
curses.cbreak();			#can exit with ^C, Don't require Enter to be hit
curses.noecho();			#Don't echo keypresses
curses.curs_set(0);			#Hide the curso (providing terminal supports it)
stdscr.move(y,x);		    #Move cursor to bottom
stdscr.addch("*");          #Add a star


#### handles user input and writing to the console
#### function is pretty much self explanitory
def  updateConsole(channel):
    global x
    global y
    direction = map[channel];
    if direction == "UP":
        if (y > 0):     #make sure we're still on the grid
            y-=1;
            stdscr.move(y,x);
            stdscr.addch("*");
            stdscr.refresh();
    if direction == "DOWN":
        if (y < HEIGHT):#make sure we're still on the grid
            y+=1;       
            stdscr.move(y,x);
            stdscr.addch("*");
            stdscr.refresh();
    if direction == "LEFT":
        if (x > 0):     #make sure we're still on the grid
            x-=1;
            stdscr.move(y,x);
            stdscr.addch("*");
            stdscr.refresh();
    if direction == "RIGHT":
        if (x < WIDTH): #make sure we're still on the grid
            x+=1;
            stdscr.move(y,x);
            stdscr.addch("*");
            stdscr.refresh();
    if direction == "CLEAR":
        stdscr.clear();
        stdscr.refresh();
    if direction == "EXIT":
        exit();
            
time.sleep(.05);
####Setup Buttons
for Button in Buttons:
    GPIO.setup(Button, GPIO.IN)
    GPIO.add_event_detect(Button, GPIO.RISING, callback=updateConsole) #Add event to Button
time.sleep(.05);

try:
    while True:
        time.sleep(500); #Allow other proccess to run
except KeyboardInterrupt:
    print("Cleaning Up");
    GPIO.cleanup();
GPIO.cleanup();

    


