#!/usr/bin/env python
# created by steve@stevesiden.com
# modified from chris@drumminhands.com
# see instructions at http://www.drumminhands.com/2014/06/15/raspberry-pi-photo-booth/

import os
import glob
import time
import traceback #?necesary?
from time import sleep
import atexit
import sys
import smtplib
import socket
from signal import alarm, signal, SIGALRM, SIGKILL


########################
### Variables Config ###
########################
total_pics = 4 # number of pics  to be taken
capture_delay = 3 # delay between pics
prep_delay = 4 # number of seconds at step 1 as users prep to have photo taken
gif_delay = 100 # How much time between frames in the animated gif
#file_path = '/home/pi/photobooth/pics/' #where do you want to save the photos
file_path = '~/home/pi/photobooth/samplepics/'

w = 800
h = 480
transform_x = 640 #how wide to scale the jpg when replaying
transfrom_y = 480 #how high to scale the jpg when replaying
offset_x = 80 #how far off to left corner to display photos
offset_y = 0 #how far off to left corner to display photos
replay_delay = 1 # how much to wait in-between showing pics on-screen after taking
replay_cycles = 4 # how many times to show each photo on-screen after taking



#################
### Functions ###
#################

def print_pics(now):  
	copypics = "cp " +file_path + now + "*.jpg "+ file_path+"PB_archive/"
	print copypics
	os.system(copypics)
	#resizing + montaging
	print "Resizing Pics..."
	#convert -resize 968x648 /home/pi/photobooth/pics/*.jpg /home/pi/photobooth/pics_tmp/*_tmp.jpg
	graphicsmagick = "gm mogrify -resize 968x648 " + file_path + now + "*.jpg" 
	print "Resizing with command: " + graphicsmagick
	os.system(graphicsmagick) #make the thumbnails

	print "Montaging Pics..."
	#montage /home/pi/photobooth/pics/*.jpg -tile 2x2 -geometry +10+10 /home/pi/temp_montage2.jpg
	graphicsmagick = "gm montage " + file_path + now + "*.jpg -tile 2x2 -geometry 1000x699+10+10 " + file_path + now + "_picmontage.jpg" 
	print "Montaging images with command: " + graphicsmagick
	os.system(graphicsmagick) 

	print "Adding Label..."
	#montage /home/pi/temp_montage2.jpg /home/pi/photobooth/photobooth_label.jpg -tile 2x1 -geometry +5+5 /home/pi/temp_montage3.jpg
	#graphicsmagick = "gm montage " + file_path + now + "_picmontage.jpg ~/home/pi/photobooth/photobooth/bn_booth_label_h.jpg -tile 1x2 -geometry +5+5 -gravity North " + file_path + now + "_labeledpicmontage.jpg" 
	
	#graphicsmagick = "gm montage " + file_path + now + "_picmontage.jpg ~/home/pi/photobooth/photobooth/bn_booth_label_h.jpg -gravity north -tile 1x2 " + file_path + now + "_picmontage_labeled.jpg"  #-geometry 968x648+10+10

	graphicsmagick = "gm convert -append ~/dev/photobooth/photobooth/bn_booth_label_h.jpg  " + file_path + now + "_picmontage.jpg " + file_path + now + "_picmontage_labeled.jpg" 
	# graphicsmagick = "gm convert \
 #    -page +0+0      "+ file_path + now + "-01.jpg \
 #    -page +978+0    "+ file_path + now + "-02.jpg \
 #    -page +0+978    "+ file_path + now + "-03.jpg \
 #    -page +978+978  "+ file_path + now + "-04.jpg \
 #    -page +1090+1360  ~/home/pi/photobooth/photobooth/bn_booth_label_h.jpg \
 #    -mosaic " + file_path + now + "_picmontage_labeled.jpg"
	print "Adding label with command: " + graphicsmagick 
	os.system(graphicsmagick) 



	#printing
	printcommand = "lp -d Canon_CP910 /home/pi/pics/print.jpg"
	os.system(printcommand) 



	
# define the photo taking function for when the big button is pressed 
def start_photobooth(): 
	################################# Begin Step 1 ################################# 
	print "Get Ready" 
	sleep (1)
	################################# Begin Step 2 #################################

	#Static Pics
	print "Finding pics" 
	#now = time.strftime("%Y%m%d%H%M%S") #get the current date and time for the start of the filename
	#now = "20150324002130"
	now = "image"
	# print "Trying to find the start images: " + file_path + "*.jpg"
	# os.rename(file_path + "*.jpg", file_path + now + "*.jpg")

	########################### Begin Step 3 #################################
	#printing pics
	print_pics(now)

	########################### Begin Step 4 #################################
	print "Done"
	print

# ####################
# ### NO GPIO - Main Program ###
# ####################
print "Photo booth app running once..." 

i = 1
while (i == 1):
		start_photobooth()
		i+=1


