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


def show_image(image_path, screen):
	#screen = init_pygame()
	img=pygame.image.load(image_path) 
	img = pygame.transform.scale(img,(transform_x,transfrom_y))
	screen.blit(img,(offset_x,offset_y))
	pygame.display.flip()


pygame.init()
#raise KeyboardInterrupt
size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
pygame.display.set_caption('Photo Booth Pics')
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

rgb = bytearray(pixel_width * pixel_height * 3)
yuv = bytearray(pixel_width * pixel_height * 3 / 2)
sizeData = [ # Camera parameters for different size settings
 # Full res      Viewfinder  Crop window
 [(1000, 666), (monitor_w, monitor_h), (0.0   , 0.0   , 1.0   , 1.0   )], # Large
 [(1920, 1080), (320, 180), (0.1296, 0.2222, 0.7408, 0.5556)], # Med
 [(1440, 1080), (320, 240), (0.2222, 0.2222, 0.5556, 0.5556)]] # Small
sizeMode = 0

screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
#background = pygame.Surface(screen.get_size())
#background = background.convert()

# Display some text
font = pygame.font.Font(None, 36)
text = font.render("Hello There", 1, (0, 200, 0))

#screen = init_pygame()
#img=pygame.image.load(image_path) 
#img = pygame.transform.scale(img,(transform_x,transfrom_y))
#screen.blit(img,(offset_x,offset_y))

sleep(2) #warm up camera

stream = io.BytesIO() # Capture into in-memory stream
camera.capture(stream, use_video_port=True, format='raw')
stream.seek(0)
stream.readinto(yuv)  # stream -> YUV buffer
stream.close()
yuv2rgb.convert(yuv, rgb, monitor_w, monitor_h)
img = pygame.image.frombuffer(rgb[0: (monitor_w * monitor_h * 3)], (monitor_w,monitor_h), 'RGB')

screen.blit(img, ((pixel_width - img.get_width() ) / 2, (pixel_height - img.get_height()) / 2))
screen.blit(text, (100,100))
pygame.display.update()

################################# Begin Step 2 #################################
print "Taking pics" 

camera.stop_preview()
camera.close()
