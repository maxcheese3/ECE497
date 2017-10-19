# Here's how to use imagemagick to display text
# Make a blank image
SIZE=320x240


TMP_FILE=/tmp/frame.png

# From: http://www.imagemagick.org/Usage/text/
modprobe fbtft_device name=adafruit28 busnum=1 rotate=270 gpios=reset:113,dc:116 cs=0
convert -background lightblue -fill blue -font mono -pointsize 24 \
      -size $SIZE \
      label:'Hello \nblah blah text \nderaileur'\
      -draw "text 0,200 'asdfasdf'" \
      $TMP_FILE

sudo fbi -noverbose -T 1 $TMP_FILE

# convert -list font