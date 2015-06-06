#!/usr/bin/env python2.7  
# script by Alex Eames http://RasPi.tv  
# http://RasPi.tv/how-to-use-interrupts-with-python-on-the-raspberry-pi-and-rpi-gpio-part-3  
import RPi.GPIO as GPIO  
GPIO.setmode(GPIO.BOARD) #physical pin numbering

button1_pin = 22 #big red button
button2_pin = 4 #exit python
button3_pin = 17 #shutdown button 
  
# button1_pin & button2_pin set up as inputs, pulled up to avoid false detection.  
# Both ports are wired to connect to GND on button press.  
# So we'll be setting up falling edge detection for both  
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)  #big red button
GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_UP)  
  
# button3_pin set up as an input, pulled down, connected to 3V3 on button press  
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  
  
# now we'll define two threaded callback functions  
# these will run in another thread when our events are detected  
def my_callback(channel):  
    print "falling edge detected on button1_pin--Big Red Button"  
  
def my_callback2(channel):  
    print "falling edge detected on button2_pin"  

  
print "Make sure you have a button connected so that when pressed"  
print "it will connect " + str(button1_pin) + " to GND\n"   
print "You will also need a second button connected so that when pressed"  
print "it will connect " + str(button2_pin) + " to GND"  
print "You will also need a third button connected so that when pressed"  
print "it will connect " + str(button3_pin) + " to 3V3 (3.3v)\n" 
raw_input("Press Enter when ready\n>")  
 

# when a falling edge is detected on button1_pin, regardless of whatever   
# else is happening in the program, the function my_callback will be run  
GPIO.add_event_detect(button1_pin, GPIO.FALLING, callback=my_callback, bouncetime=300)  
  
# when a falling edge is detected on button2_pin, regardless of whatever   
# else is happening in the program, the function my_callback2 will be run  
# 'bouncetime=300' includes the bounce control written into interrupts2a.py  
GPIO.add_event_detect(button2_pin, GPIO.FALLING, callback=my_callback2, bouncetime=300)  
  
try:  
   print "Waiting for rising edge on button3_pin"  
   GPIO.wait_for_edge(button3_pin, GPIO.RISING)  
   print "Rising edge detected on " + str(button3_pin) + ". Here endeth the third lesson."  
  
except KeyboardInterrupt:  
   GPIO.cleanup()       # clean up GPIO on CTRL+C exit  
GPIO.cleanup()           # clean up GPIO on normal exit