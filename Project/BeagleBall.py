#!/usr/bin/env python3
import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.ADC as ADC
import time, math
import getopt, sys
# import rcpy library
# This automatically initizalizes the robotics cape
import rcpy 
import rcpy.servo as servo
import rcpy.clock as clock
import io
import Adafruit_BBIO.PWM as PWM

#Import stuff for flite
from subprocess import call
import os

LEDs = ["USR0","USR1","USR2","USR3"];
#LEDs = ["GP1_3","GP1_4","RED","GREEN"];
Buttons = ["GP1_4","GP1_3"];#,"GP0_5","GP0_6"];
Sensor = "GP0_5";
#map = {Buttons[0]:LEDs[0], Buttons[1]:LEDs[1], Buttons[0]:LEDs[2], Buttons[1]:LEDs[3]}


#Servo Defaults
duty = 1.5
period = 0.02
channel = 1

brk = False
free = False
# set state to rcpy.RUNNING
rcpy.set_state(rcpy.RUNNING)

lFlipOff=True;
rFlipOff=True;

lServo = servo.Servo(1);
rServo = servo.Servo(4);
#servo.enable();
lclock = clock.Clock(lServo, period)
rclock = clock.Clock(rServo, period)
lclock.start();
rclock.start();
servo.enable();
# ADC.setup();
Flippers = ["GP0_3","GP0_4"];#"AIN0","AIN1"];
Servos = [lServo,rServo]
map = {Flippers[0]:Servos[0], Flippers[1]:Servos[1]};#, Buttons[2]:LEDs[2], Buttons[3]:LEDs[3]};#, Flippers[0]:Servos[0], Flippers[1]:Servos[1]};

voice = "rms";  #Voice for flite


file = open('highScore.txt', 'r+');
highScore = file.readline();
print("\n\n\n\n\n\nWelcome to BeagleBall.  The High Score is: " + str(highScore));
score = 0;

#PWM.start("P8_13", 95.0, 60,1)
#PWM.set_duty_cycle("P8_13", 97.0)
#PWM.stop("P8_13")
#PWM.cleanup()




def buttonHit(channel):
    # state = GPIO.input(channel);
    # GPIO.output(map[channel], state);
    # print(map[channel] + " Hit!");
    # GPIO.output(map[channel], 0);
    global score;
    score +=1;
    print("Point! Score is now: " + str(score));

    
    #speak("Score!");
    
def sensorHit(channel):
    #print("ball detected");
    global score;
    global highScore;
    global file;
    if(score>int(highScore)):
        file.close();
        file = open('highScore.txt','w+');
        file.write(str(score));
        file.close();
        file = open('highScore.txt', 'r+');
        highScore = file.readline();
        print("You got a High Score!!  " + highScore);
    else:
        score = 0;
    print("You lose, score set to 0 :(");
    time.sleep(1);
    print("Reset Ball")

def flipperChoose(Flipper):
    if GPIO.input(Flipper) == 1:
        flipperReleased(Flipper);
        print("released" + Flipper)
    else:
        print("pressed" + Flipper)
        flipperHit(Flipper);
    time.sleep(.025);
    
def flipperHit(channel):
    if(channel==Flippers[0]):
        map[channel].set(1.4);
    elif(channel==Flippers[1]):
        map[channel].set(0);

    
def flipperReleased(channel):
    if (channel==Flippers[0]):
        map[channel].set(0);
    elif(channel==Flippers[1]):
        map[channel].set(1.4);

    
def speak(output):
    call(["flite", "-voice", voice, "-t", output])
    
def main():
    delay = 0.1;    
    #Setup LEDs
    for LED in LEDs:
        GPIO.setup(LED, GPIO.OUT)   #Setup LED for output
    time.sleep(.05);
    
    ####Setup Buttons
    for Button in Buttons:
        GPIO.setup(Button, GPIO.IN);
        GPIO.add_event_detect(Button, GPIO.RISING, callback=buttonHit) #Add event to Button
    time.sleep(.05);
    
    ####Setup Buttons
    for Button in Flippers:
        GPIO.setup(Button, GPIO.IN);
        GPIO.add_event_detect(Button, GPIO.BOTH, callback=flipperChoose) #Add event to Button
    time.sleep(.05);
    
    GPIO.setup(Sensor, GPIO.IN);
    GPIO.add_event_detect(Sensor, GPIO.RISING, callback=sensorHit) #Add event to Button
    
    
    
    print("Play Ball!");
    #speak("Play Ball!");

    try:
        while True:

            time.sleep(.1); #Allow other proccess to run

                
    except KeyboardInterrupt:
        print("Cleaning Up");
        GPIO.cleanup();
        # stop clock
        lclock.stop();
        rclock.stop();
    
        # disable servos
        servo.disable();
        
    GPIO.cleanup();
    # stop clock
    lclock.stop();
    rclock.stop();
    
    # disable servos
    servo.disable();
    
if __name__ == "__main__":
    main()
