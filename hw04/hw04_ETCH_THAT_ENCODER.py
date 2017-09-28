############################################
# HW04_ETCH_THAT_ENCODER.py
# Simple 8x8 LED matrix drawing program created by Ryan Evans.
# Controls are encoders for movement.
# PAUSE clears
# MODE exits
# Has configureable WIDTH and HEIGHT settings.
# Run with python3 HW02_ETCH_A_SKETCH.py
# September 26, 2017
############################################

#!/usr/bin/env python3s
import Adafruit_BBIO.GPIO as GPIO
import time
import smbus
bus = smbus.SMBus(1)  # Use i2c bus 1
matrix = 0x70         # Use address 0x70
# import rcpy library
# This automatically initizalizes the robotics cape
import rcpy 
import rcpy.encoder as encoder

rcpy.set_state(rcpy.RUNNING)
print("Press Ctrl-C to exit")

delay = 1; # Delay between images in s

bus.write_byte_data(matrix, 0x21, 0)   # Start oscillator (p10)
bus.write_byte_data(matrix, 0x81, 0)   # Disp on, blink off (p11)
bus.write_byte_data(matrix, 0xe7, 0)   # Full brightness (page 15)

# The first byte is GREEN, the second is RED.
# Set board to have top left LED on
board = [0b10000000, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00
]


WIDTH = 7;			#Number of columns
HEIGHT = 7;		#Number of rows
global x;
x = 0;			    #Cursor x coordinate
global y;
y = HEIGHT;			#Cursor y coordinate
global leftEnc;
leftEnc = 0;
global rightEnc;
rightEnc = 0;

GPIO.setup("PAUSE", GPIO.IN);
GPIO.setup("MODE", GPIO.IN);
#### handles user input and writing to the LEDmatrix
#### uses bitwise shifting to turn on the right LED's
#### function is pretty much self explanitory
#### has repeated code, could be made into new function
def  updateLEDs(channel):
    global x
    global y
    global board
    direction = channel;
    if direction == "DOWN":
        if (y > 0):     #make sure we're still on the grid
            y-=1;
    if direction == "UP":
        if (y < HEIGHT):#make sure we're still on the grid
            y+=1;       
    if direction == "LEFT":
        if (x > 0):     #make sure we're still on the grid
            x-=1;
    if direction == "RIGHT":
        if (x < WIDTH): #make sure we're still on the grid
            x+=1;

    if direction == "CLEAR":
        #Reset board
        board = [0b00000000, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00
        ]
        bus.write_i2c_block_data(matrix, 0, board)
    if direction == "EXIT":
        boardReset = [0b00000000, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00
        ]
        bus.write_i2c_block_data(matrix, 0, boardReset)
        exit();
    board[x*2] = board[x*2] | 1<<y;
    bus.write_i2c_block_data(matrix, 0, board)
            
time.sleep(.05);
bus.write_i2c_block_data(matrix, 0, board)

try:
    # keep running
    while True:
        # running
        if rcpy.get_state() == rcpy.RUNNING:
            e2 = encoder.get(2) # read the encoders
            e3 = encoder.get(3)
            if(e2 > leftEnc+2):
                #Left enc moved left
                updateLEDs("DOWN")
            elif(e2 < leftEnc-2):
                #Left enc moved right
                updateLEDs("UP")
            if(e3 > rightEnc+2):
                #Right enc moved left
                updateLEDs("LEFT")
            elif(e3 < rightEnc-2):
                #Right enc moved left
                updateLEDs("RIGHT")
            if (GPIO.input("PAUSE")==0):
                updateLEDs("CLEAR")
            if (GPIO.input("MODE")==0):
                updateLEDs("EXIT")

            #set new enc position to global enc position
            leftEnc=e2;
            rightEnc=e3;

            print('\r {:+6d} | {:+6d}'.format(e2,e3), end='')
        time.sleep(.1)  # sleep some

except KeyboardInterrupt:
    # Catch Ctrl-C
    pass

finally:
    print("\nBye BeagleBone!")