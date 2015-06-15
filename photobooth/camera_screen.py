#!/usr/bin/env python
# created by steve@stevesiden.com
# modified from chris@drumminhands.com
# see instructions at http://www.drumminhands.com/2014/06/15/raspberry-pi-photo-booth/

import os
import glob
import time
import traceback
from time import sleep
import RPi.GPIO as GPIO #using physical pin numbering change in future?
import picamera # http://picamera.readthedocs.org/en/release-1.4/install2.html
import atexit
import sys, getopt
import socket
import pygame
import cups
import io, yuv2rgb
import Image, ImageDraw
#import pytumblr # https://github.com/tumblr/pytumblr
#from twython import Twython
import config
import shutil
from signal import alarm, signal, SIGALRM, SIGKILL
import Image, ImageDraw


def show_image(image_path, screen):
	#screen = init_pygame()
	img=pygame.image.load(image_path) 
	img = pygame.transform.scale(img,(transform_x,transfrom_y))
	screen.blit(img,(offset_x,offset_y))
	pygame.display.flip()

real_path = os.path.dirname(os.path.realpath(__file__))

########################
### Variables Config ###
########################

post_online = 0 # default 1. Change to 0 if you don't want to upload pics.
total_pics = 4 # number of pics to be taken
capture_delay = 2 # delay between pics
prep_delay = 5 # number of seconds at step 1 as users prep to have photo taken
gif_delay = 50 # How much time between frames in the animated gif
restart_delay = 5 # how long to display finished message before beginning a new session

monitor_w = 800 #800
monitor_h = 480 #480
transform_x = 640 #640 # how wide to scale the jpg when replaying
transfrom_y = 480 #480 # how high to scale the jpg when replaying
offset_x = 40 # how far off to left corner to display photos
offset_y = 0 # how far off to left corner to display photos
replay_delay = 1 # how much to wait in-between showing pics on-screen after taking
replay_cycles = 1 # how many times to show each photo on-screen after taking




#disp_no = os.getenv("DISPLAY")
#if disp_no:
#    print "I'm running under X display = {0}".format(disp_no)

# Check which frame buffer drivers are available
# Start with fbcon since directfb hangs with composite output
drivers = ['fbcon', 'directfb', 'svgalib']
found = False
for driver in drivers:
    # Make sure that SDL_VIDEODRIVER is set
    if not os.getenv('SDL_VIDEODRIVER'):
        os.putenv('SDL_VIDEODRIVER', driver)
    try:
        pygame.display.init()
    except pygame.error:
        print 'Driver: {0} failed.'.format(driver)
        continue
    found = True
    break

if not found:
    raise Exception('No suitable video driver found!')





pygame.init()
#raise KeyboardInterrupt
size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
#pygame.display.set_caption('Photo Booth Pics')
pygame.mouse.set_visible(False) #hide the mouse cursor	
screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
################################# Begin Step 1 ################################# 
show_image(real_path + "/assets/blank.png", screen)
print "Get Ready"

show_image(real_path + "/assets/instructions.png", screen)
sleep(prep_delay)

show_image(real_path + "/assets/blank.png", screen)







camera = picamera.PiCamera()
pixel_width = 1000 #originally 500: use a smaller size to process faster, and tumblr will only take up to 500 pixels wide for animated gifs
#pixel_height = monitor_h * pixel_width // monitor_w #optimize for monitor size
pixel_height = 666
camera.resolution = (pixel_width, pixel_height) 
camera.vflip = False
camera.hflip = False
#camera.start_preview()

# prep a byte array to store captured image
rgb = bytearray(camera.resolution[0] * camera.resolution[1] * 3)




# Display some text
font = pygame.font.Font(None, 36)
text = font.render("Hello There", 1, (0, 200, 0))


stream = io.BytesIO()
camera.capture(stream, use_video_port=True, format='rgb', resize=(monitor_w, monitor_h))
stream.seek(0)
stream.readinto(rgb)
stream.close()

img = pygame.image.frombuffer(rgb[0:(monitor_w * monitor_h * 3)], (monitor_w, monitor_h), 'RGB')
screen.blit(img,(offset_x,offset_y))

screen.blit(text, (monitor_w/2,monitor_h/2))
pygame.display.update()
print "Taking pics" 
now = time.strftime("%Y-%m-%d-%H:%M:%S") #get the current date and time for the start of the filename
try: #take the photos
	#for i, filename in enumerate(camera.capture_continuous(config.file_path + now + '-' + '{counter:02d}.jpg')):
	for i in range(0, total_pics):
		filename = config.file_path + now + '-0' + str(i+1) + '.jpg'
		camera.capture(filename)
		GPIO.output(led2_pin,True) #turn on the LED
		print(filename)
		sleep(0.25) #pause the LED on for just a bit
		GPIO.output(led2_pin,False) #turn off the LED
		img = pygame.image.load(filename)
    		screen.blit(img, (0, 0))
		pygame.display.update()
		sleep(capture_delay) # pause in-between shots
		if i == total_pics-1:
			break

finally:

	camera.stop_preview()
	camera.close()



