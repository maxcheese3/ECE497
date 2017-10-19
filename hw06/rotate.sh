#!/bin/sh

# Export Rotate
sudo bash << EOF
    # Save contents of framebuffer
    cat /dev/fb0 > /tmp/fb0
    # Disable the framebuffer
    echo Disabling framebuffer
    rmmod fbtft_device
    sleep 1
    # Get access to the RESET pin
    echo 113  > /sys/class/gpio/export # RESET - V14 - GP0_PIN4
    echo Toggling RESET
    sleep 1
    # Toggle it
    echo out > /sys/class/gpio/gpio113/direction
    echo 0   > /sys/class/gpio/gpio113/value
    echo 1   > /sys/class/gpio/gpio113/value
    
    # Remove access so the framebuffer can use it
    echo 113  > /sys/class/gpio/unexport # RESET - V14 - GP0_PIN4

    # Fire up the framebuffer
    echo Firing up framebuffer
    sleep 1
    #rotate by changing the value of rotate in the following line
    modprobe fbtft_device name=adafruit28 busnum=1 rotate=90 gpios=reset:113,dc:116 cs=0
    sudo fbi -noverbose -T 1 -a boris_education.png

    # Restore the image
    cat /tmp/fb0 > /dev/fb0
EOF
