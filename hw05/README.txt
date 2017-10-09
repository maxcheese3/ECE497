1.Before writing any code, write a paragraph describing how boneServer.js and the browser interact in the given example. For example, in matrixLED.js connect() is called to make a connection between the browser and the bone.  The message “matrix” is sent to the bone. What happens in response to the message?

When "matrix" is sent, boneServer.js recieves it.  It then executes a child process initiating i2c stuff.


2.What happens when an “LED” is clicked on in the browser?
It calls i2cset, and sets the right register based on the coordinates of the button.

3.What entry in matrix.css is used to color the LED?
.LED

4.Write a high level paragraph about how you will control the two LEDs. What messages will be sent between the browser and the bone?
I'm going to modify the matrixLED.css class to include three levels of being on.  Green, Orange, and Red.

5.Write your code.  Do you need to change boneServer.js? (I don’t think so.)  Customize the html to have your name on it, etc.
no


-----------------------------------
Run boneServer.js just like normal.
Modifications have been made to matrixLED.js
and matrixLED.css

# Comments from Prof. Yoder
# Found your answers to the questions.  "stuff" is a bit broad.
# Thanks for the demo.
# Grade:  10/10