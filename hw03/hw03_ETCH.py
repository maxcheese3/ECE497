############################################
# HW03_ETCH.py
# Simple 8x8 LED matrix drawing program created by Ryan Evans.
# Controls are buttons conencted to GP0 for movement.
# PAUSE clears
# MODE exits
# Has configureable WIDTH and HEIGHT settings.
# Run with python3 HW02_ETCH_A_SKETCH.py
# September 19, 2017
############################################

#!/usr/bin/env python3s
import Adafruit_BBIO.GPIO as GPIO
import time
import smbus
import curses
bus = smbus.SMBus(1)  # Use i2c bus 1
matrix = 0x70         # Use address 0x70

delay = 1; # Delay between images in s

bus.write_byte_data(matrix, 0x21, 0)   # Start oscillator (p10)
bus.write_byte_data(matrix, 0x81, 0)   # Disp on, blink off (p11)
bus.write_byte_data(matrix, 0xe7, 0)   # Full brightness (page 15)

# The first byte is GREEN, the second is RED.
# Set board to have top left LED on
board = [0b10000000, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00
]

Buttons = ["GP0_3","GP0_4","GP0_5","GP0_6","PAUSE","MODE"];
map = {Buttons[0]:"RIGHT", Buttons[1]:"UP", Buttons[2]:"DOWN", Buttons[3]:"LEFT", Buttons[4]:"CLEAR",Buttons[5]:"EXIT"}


WIDTH = 7;			#Number of columns
HEIGHT = 7;		#Number of rows
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


#### handles user input and writing to the LEDmatrix
#### uses bitwise shifting to turn on the right LED's
#### function is pretty much self explanitory
#### has repeated code, could be made into new function
def  updateConsole(channel):
    global x
    global y
    global board
    direction = map[channel];
    if direction == "DOWN":
        if (y > 0):     #make sure we're still on the grid
            y-=1;
    if direction == "UP":
        if (y < HEIGHT):#make sure we're still on the grid
            y+=1;       
            board[x*2] =board[x*2]| 1<<y;
    if direction == "LEFT":
        if (x > 0):     #make sure we're still on the grid
            x-=1;
    if direction == "RIGHT":
        if (x < WIDTH): #make sure we're still on the grid
            x+=1;

    if direction == "CLEAR":
        #Reset board
        board = [0b10000000, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00
        ]
        bus.write_i2c_block_data(matrix, 0, board)
        #reset x and y
        x=0
        y=HEIGHT
        return
    if direction == "EXIT":
        boardReset = [0b00000000, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00
        ]
        bus.write_i2c_block_data(matrix, 0, boardReset)
        exit();
    board[x*2] = board[x*2] | 1<<y;
    bus.write_i2c_block_data(matrix, 0, board)
    print(x,y)
            
time.sleep(.05);
####Setup Buttons
for Button in Buttons:
    GPIO.setup(Button, GPIO.IN)
    GPIO.add_event_detect(Button, GPIO.RISING, callback=updateConsole) #Add event to Button
time.sleep(.05);
bus.write_i2c_block_data(matrix, 0, board)

try:
    while True:
        time.sleep(1000); #Allow other proccess to run
except KeyboardInterrupt:
    print("Cleaning Up");
    GPIO.cleanup();
GPIO.cleanup();