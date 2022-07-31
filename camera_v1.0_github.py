# Paparzzo C/CS 12MP Camera v1.0
# Raspberry pi camera
#
# records pictures and 5 minute max video clips (no audio in this version)
#
# This camera requires 4 GPIO buttons
# 
# Runs on pygame and python3
#
# Author:			Billy O Sullivan
# Created date:		08 June 2022
# Edited:			31 July 2022
#
# python 3.10
#
#
# requires MP4Box
# sudo apt install -y gpac
#
# you can change the GPIO pins to whatever you prefer
# 
#
#############
#
# be sure to change the file paths to what you have on your own raspberry pi
#
##############
#
# Directory Layout
#
# I have my directory layout as follows (deviation will require changes to the code!!!)
#
# main directory
# /home/billy/Desktop/camera
# in here place the camera_settings file
# camera python file
# rec.png file
#
# /home/billy/Desktop/camera/photos/
# your photos are saved here
#
# /home/billy/Desktop/camera/videos/
# your videos are saved here
# 
######################################################################################

# import libraries
from picamera import PiCamera
import time 
from datetime import datetime
import RPi.GPIO as GPIO
import pygame
import os
import subprocess
import shlex
from PIL import Image, ImageDraw, ImageFont

# setup gpio buttons
# GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False) # Ignore warning

# set GPIO Pins
snap = 14
up = 12
down = 23
select = 25

# set GPIO direction (IN / OUT)
GPIO.setup(snap, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(up, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(down, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(select, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# define some colours for pygame incase  i want them
GREEN = (0, 128, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (173,255,47)
RED = (255,0,0)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 480


# this is the menu function used to go to various settings and change settings
def menu(screen):

	time.sleep(.5)
	opt = 1
	row = 25

	# settings text file to store settings after reboot
	with open("/home/billy/Desktop/camera/camera_settings.txt", "r") as settings:
		for line in settings:
			#print(line)
			if "mode" in line:
				modeopt = line.split()[1]
				mode_setting = "mode = " + str(modeopt)
			if "brightness" in line:
				brightnessopt = line.split()[1]
				bright_setting = "brightness = " + str(brightnessopt)
			if "contrast" in line:
				contrastopt = line.split()[1]
				cont_setting = "contrast = " + str(contrastopt)
			if "exposure" in line:
				exposureopt = line.split()[1]
				expo_setting = "exposure = " + exposureopt
			if "white" in line:
				whiteopt = line.split()[1]
				white_setting = "white balance = " + whiteopt
			if "effect" in line:
				effectopt = line.split()[1]
				effect_setting = "effect = " + effectopt

	settings.close()

	while 1:
		screen.fill(BLACK)
		font = pygame.font.SysFont(None, 30)
		menu_list1 = font.render('mode', True, WHITE)
		menu_list2 = font.render('brightness', True, WHITE)
		menu_list3 = font.render('contrast', True, WHITE)
		menu_list4 = font.render('exposure', True, WHITE)
		menu_list5 = font.render('white balance', True, WHITE)
		menu_list6 = font.render('effects', True, WHITE)
		menu_list7 = font.render('view pictures', True, WHITE)
		menu_list8 = font.render('exit', True, WHITE)
		screen.blit(menu_list1, (60, 20))
		screen.blit(menu_list2, (60, 45))
		screen.blit(menu_list3, (60, 70))
		screen.blit(menu_list4, (60, 95))
		screen.blit(menu_list5, (60, 120))
		screen.blit(menu_list6, (60, 145))
		screen.blit(menu_list7, (60, 170))
		screen.blit(menu_list8, (60, 195))

		settings_list0 = font.render("Current Settings", True, GREEN)
		settings_list1 = font.render(mode_setting, True, GREEN)
		settings_list2 = font.render(bright_setting, True, GREEN)
		settings_list3 = font.render(cont_setting, True, GREEN)
		settings_list4 = font.render(expo_setting, True, GREEN)
		settings_list5 = font.render(white_setting, True, GREEN)
		settings_list6 = font.render(effect_setting, True, GREEN)
		screen.blit(settings_list0, (60, 220))
		screen.blit(settings_list1, (60, 245))
		screen.blit(settings_list2, (60, 270))
		screen.blit(settings_list3, (60, 295))
		screen.blit(settings_list4, (60, 320))
		screen.blit(settings_list5, (60, 345))
		screen.blit(settings_list6, (60, 370))


		# up button selection
		if GPIO.input(up) == GPIO.LOW and opt == 1:
			time.sleep(.5)
			opt = 2
			row = 50
		if GPIO.input(up) == GPIO.LOW and opt == 2:
			time.sleep(.5)
			opt = 3
			row = 75
		if GPIO.input(up) == GPIO.LOW and opt == 3:
			time.sleep(.5)
			opt = 4
			row = 100
		if GPIO.input(up) == GPIO.LOW and opt == 4:
			time.sleep(.5)
			opt = 5
			row = 125
		if GPIO.input(up) == GPIO.LOW and opt == 5:
			time.sleep(.5)
			opt = 6
			row = 150
		if GPIO.input(up) == GPIO.LOW and opt == 6:
			time.sleep(.5)
			opt = 7
			row = 175
		if GPIO.input(up) == GPIO.LOW and opt == 7:
			time.sleep(.5)
			opt = 8
			row = 195
		if GPIO.input(up) == GPIO.LOW and opt == 8:
			time.sleep(.5)
			opt = 1
			row = 25			

		# down button selection
		if GPIO.input(down) == GPIO.LOW and opt == 1:
			time.sleep(.5)
			opt = 8
			row = 195
		if GPIO.input(down) == GPIO.LOW and opt == 2:
			time.sleep(.5)
			opt = 1
			row = 25
		if GPIO.input(down) == GPIO.LOW and opt == 3:
			time.sleep(.5)
			opt = 2
			row = 50
		if GPIO.input(down) == GPIO.LOW and opt == 4:
			time.sleep(.5)
			opt = 3
			row = 75
		if GPIO.input(down) == GPIO.LOW and opt == 5:
			time.sleep(.5)
			opt = 4
			row = 100
		if GPIO.input(down) == GPIO.LOW and opt == 6:
			time.sleep(.5)
			opt = 5
			row = 125
		if GPIO.input(down) == GPIO.LOW and opt == 7:
			time.sleep(.5)
			opt =  6
			row = 150
		if GPIO.input(down) == GPIO.LOW and opt == 8:
			time.sleep(.5)
			opt =  7
			row = 175

		pygame.draw.rect(screen, RED, pygame.Rect(250, row, 20, 20))

		# select key pressed
		if GPIO.input(select) == GPIO.LOW and opt == 1:
			time.sleep(.5)
			mode(screen)
		if GPIO.input(select) == GPIO.LOW and opt == 2:
			time.sleep(.5)
			brightness(screen)
		if GPIO.input(select) == GPIO.LOW and opt == 3:
			time.sleep(.5)
			contrast(screen)
		if GPIO.input(select) == GPIO.LOW and opt == 4:
			time.sleep(.5)
			exposure(screen)
		if GPIO.input(select) == GPIO.LOW and opt == 5:
			time.sleep(.5)
			white_balance(screen)
		if GPIO.input(select) == GPIO.LOW and opt == 6:
			time.sleep(.5)
			effects(screen)
		if GPIO.input(select) == GPIO.LOW and opt == 7:
			time.sleep(.5)
			picview(screen)
		if GPIO.input(select) == GPIO.LOW and opt == 8:
			time.sleep(.5)
			main()
		
		pygame.display.flip()


# function for capture modes - single, burst or video to begin with
# single mode takes a picture and sleeps for 2 seconds
# burst mode takes 5 pictures, 1 every 250 milliseconds
# video will record video when snap is pressed and stop when snap is pressed again
def mode(screen):
	
	opt = 1
	row = 25
	time.sleep(.5)
	mode = 1

	while 1:
		screen.fill(BLACK)
		font = pygame.font.SysFont(None, 30)
		menu_list1 = font.render('mode 1: single picture', True, WHITE)
		menu_list2 = font.render('mode 2: burst 5 pictures', True, WHITE)
		menu_list3 = font.render('mode 3: video', True, WHITE)
		menu_list4 = font.render('exit', True, WHITE)
		screen.blit(menu_list1, (60, 20))
		screen.blit(menu_list2, (60, 45))
		screen.blit(menu_list3, (60, 70))
		screen.blit(menu_list4, (60, 95))
		
		# up button selection
		if GPIO.input(up) == GPIO.LOW and opt == 1:
			time.sleep(.5)
			opt = 2
			row = 50
		if GPIO.input(up) == GPIO.LOW and opt == 2:
			time.sleep(.5)
			opt = 3
			row = 75
		if GPIO.input(up) == GPIO.LOW and opt == 3:
			time.sleep(.5)
			opt = 4
			row = 100
		if GPIO.input(up) == GPIO.LOW and opt == 4:
			time.sleep(.5)
			opt = 1
			row = 25
		
		# down button selection
		if GPIO.input(down) == GPIO.LOW and opt == 1:
			time.sleep(.5)
			opt = 4
			row = 100
		if GPIO.input(down) == GPIO.LOW and opt == 2:
			time.sleep(.5)
			opt = 1
			row = 25
		if GPIO.input(down) == GPIO.LOW and opt == 3:
			time.sleep(.5)
			opt = 2
			row = 50
		if GPIO.input(down) == GPIO.LOW and opt == 4:
			time.sleep(.5)
			opt = 3
			row = 75

		pygame.draw.rect(screen, RED, pygame.Rect(350, row, 20, 20))

		# select key pressed
		if GPIO.input(select) == GPIO.LOW and opt == 1:
			time.sleep(.5)
			newfile = ""
			with open("/home/billy/Desktop/camera/camera_settings.txt", "r") as settings:
				for line in settings:
					if "mode" in line:
						data = line.split()[1]
						line = line.replace(data, "1")
					newfile += line + "\n"
			settings.close()
			new_settings = open("/home/billy/Desktop/camera/camera_settings.txt", "w")
			new_settings.write(newfile)
			new_settings.close()
			menu_list5 = font.render('mode = 1', True, WHITE)
			screen.blit(menu_list5, (60, 145))
			time.sleep(2)
		if GPIO.input(select) == GPIO.LOW and opt == 2:
			time.sleep(.5)
			newfile = ""
			with open("/home/billy/Desktop/camera/camera_settings.txt", "r") as settings:
				for line in settings:
					if "mode" in line:
						data = line.split()[1]
						line = line.replace(data, "2")
					newfile += line + "\n"
			settings.close()
			new_settings = open("/home/billy/Desktop/camera/camera_settings.txt", "w")
			new_settings.write(newfile)
			new_settings.close()
			menu_list5 = font.render('mode = 2', True, WHITE)
			screen.blit(menu_list5, (60, 145))
			time.sleep(2)
		if GPIO.input(select) == GPIO.LOW and opt == 3:
			time.sleep(.5)
			newfile = ""
			with open("/home/billy/Desktop/camera/camera_settings.txt", "r") as settings:
				for line in settings:
					if "mode" in line:
						data = line.split()[1]
						line = line.replace(data, "3")
					newfile += line + "\n"
			settings.close()
			new_settings = open("/home/billy/Desktop/camera/camera_settings.txt", "w")
			new_settings.write(newfile)
			new_settings.close()
			menu_list5 = font.render('mode = 3', True, WHITE)
			screen.blit(menu_list5, (60, 145))
			time.sleep(2)
		if GPIO.input(select) == GPIO.LOW and opt == 4:
			time.sleep(.5)
			menu(screen)

		pygame.display.flip()		

# this function sets the brightness of the preview screen (and picture)
# by default it is set to 50%
def brightness(screen):

	opt = 50
	time.sleep(.5)
	while 1:
		screen.fill(BLACK)
		font = pygame.font.SysFont(None, 30)
		menu_list1 = font.render('brightness:', True, WHITE)
		menu_list2 = font.render('press select to exit', True, WHITE)
		menu_list3 = font.render(str(opt), True, WHITE)
		screen.blit(menu_list1, (60, 20))
		screen.blit(menu_list2, (60, 45))
		screen.blit(menu_list3, (200, 20))

		# up button selection
		if GPIO.input(up) == GPIO.LOW and opt < 101:
			time.sleep(.25)
			opt = opt + 5
		if GPIO.input(up) == GPIO.LOW and opt > 100:
			time.sleep(.25)
			opt = 0
			
		# down button selection
		if GPIO.input(down) == GPIO.LOW and opt > 0:
			time.sleep(.25)
			opt = opt - 5
		if GPIO.input(down) == GPIO.LOW and opt < 1:
			time.sleep(.25)
			opt = 100

		if GPIO.input(select) == GPIO.LOW:
			time.sleep(.5)
			newfile = ""
			with open("/home/billy/Desktop/camera/camera_settings.txt", "r") as settings:
				for line in settings:
					if "brightness" in line:
						data = line.split()[1]
						line = line.replace(data, str(opt))
					newfile += line + "\n"
			settings.close()
			new_settings = open("/home/billy/Desktop/camera/camera_settings.txt", "w")
			new_settings.write(newfile)
			new_settings.close()
			menu(screen)

		pygame.display.flip()	


# this is used to set the contrast
#by default it is set to 50%
def contrast(screen):
	
	opt = 50
	time.sleep(.5)
	while 1:
		screen.fill(BLACK)
		font = pygame.font.SysFont(None, 30)
		menu_list1 = font.render('contrast:', True, WHITE)
		menu_list2 = font.render('press select to exit', True, WHITE)
		menu_list3 = font.render(str(opt), True, WHITE)
		screen.blit(menu_list1, (60, 20))
		screen.blit(menu_list2, (60, 45))
		screen.blit(menu_list3, (160, 20))

		# up button selection
		if GPIO.input(up) == GPIO.LOW and opt < 101:
			time.sleep(.25)
			opt = opt + 5
		if GPIO.input(up) == GPIO.LOW and opt > 100:
			time.sleep(.25)
			opt = 0			

		# down button selection
		if GPIO.input(down) == GPIO.LOW and opt > 0:
			time.sleep(.25)
			opt = opt - 5
		if GPIO.input(down) == GPIO.LOW and opt < 1:
			time.sleep(.25)
			opt = 100

		if GPIO.input(select) == GPIO.LOW:
			time.sleep(.5)
			newfile = ""
			with open("/home/billy/Desktop/camera/camera_settings.txt", "r") as settings:
				for line in settings:
					if "contrast" in line:
						data = line.split()[1]
						line = line.replace(data, str(opt))
					newfile += line + "\n"
			settings.close()
			new_settings = open("/home/billy/Desktop/camera/camera_settings.txt", "w")
			new_settings.write(newfile)
			new_settings.close()
			menu(screen)

		pygame.display.flip()


# this is used to set the eposure of the camera
# exposure is the amount of light that reaches your cameras sensor
# by default it is set to auto
def exposure(screen):

	opt = 1
	row = 50
	time.sleep(.5)
	while 1:
		screen.fill(BLACK)
		font = pygame.font.SysFont(None, 30)
		menu_list1 = font.render('Exposure Mode', True, WHITE)
		menu_list2 = font.render('auto', True, WHITE)
		menu_list3 = font.render('off', True, WHITE)
		menu_list4 = font.render('night', True, WHITE)
		menu_list5 = font.render('snow', True, WHITE)
		menu_list6 = font.render('beach', True, WHITE)
		menu_list7 = font.render('antishake', True, WHITE)
		screen.blit(menu_list1, (60, 20))
		screen.blit(menu_list2, (60, 45))
		screen.blit(menu_list3, (60, 70))
		screen.blit(menu_list4, (60, 95))
		screen.blit(menu_list5, (60, 120))
		screen.blit(menu_list6, (60, 145))
		screen.blit(menu_list7, (60, 170))
		

		# up button selection
		if GPIO.input(up) == GPIO.LOW and opt == 1:
			time.sleep(.5)
			opt = 2
			row = 75
		if GPIO.input(up) == GPIO.LOW and opt == 2:
			time.sleep(.5)
			opt = 3
			row = 100
		if GPIO.input(up) == GPIO.LOW and opt == 3:
			time.sleep(.5)
			opt = 4
			row = 125
		if GPIO.input(up) == GPIO.LOW and opt == 4:
			time.sleep(.5)
			opt = 5
			row = 150
		if GPIO.input(up) == GPIO.LOW and opt == 5:
			time.sleep(.5)
			opt = 6
			row = 175
		if GPIO.input(up) == GPIO.LOW and opt == 6:
			time.sleep(.5)
			opt = 1
			row = 50
			
		# down button selection
		if GPIO.input(down) == GPIO.LOW and opt == 1:
			time.sleep(.5)
			opt = 6
			row = 175
		if GPIO.input(down) == GPIO.LOW and opt == 2:
			time.sleep(.5)
			opt = 1
			row = 50
		if GPIO.input(down) == GPIO.LOW and opt == 3:
			time.sleep(.5)
			opt = 2
			row = 75
		if GPIO.input(down) == GPIO.LOW and opt == 4:
			time.sleep(.5)
			opt = 3
			row = 100
		if GPIO.input(down) == GPIO.LOW and opt == 5:
			time.sleep(.5)
			opt = 4
			row = 125
		if GPIO.input(down) == GPIO.LOW and opt == 6:
			time.sleep(.5)
			opt = 5
			row = 150
			
		pygame.draw.rect(screen, RED, pygame.Rect(350, row, 20, 20))

		# select key pressed
		if GPIO.input(select) == GPIO.LOW and opt == 1:
			time.sleep(.5)
			newfile = ""
			with open("/home/billy/Desktop/camera/camera_settings.txt", "r") as settings:
				for line in settings:
					if "exposure" in line:
						data = line.split()[1]
						line = line.replace(data, "auto")
					newfile += line + "\n"
			settings.close()
			new_settings = open("/home/billy/Desktop/camera/camera_settings.txt", "w")
			new_settings.write(newfile)
			new_settings.close()
			menu(screen)
		if GPIO.input(select) == GPIO.LOW and opt == 2:
			time.sleep(.5)
			newfile = ""
			with open("/home/billy/Desktop/camera/camera_settings.txt", "r") as settings:
				for line in settings:
					if "exposure" in line:
						data = line.split()[1]
						line = line.replace(data, "off")
					newfile += line + "\n"
			settings.close()
			new_settings = open("/home/billy/Desktop/camera/camera_settings.txt", "w")
			new_settings.write(newfile)
			new_settings.close()
			menu(screen)
		if GPIO.input(select) == GPIO.LOW and opt == 3:
			time.sleep(.5)
			newfile = ""
			with open("/home/billy/Desktop/camera/camera_settings.txt", "r") as settings:
				for line in settings:
					if "exposure" in line:
						data = line.split()[1]
						line = line.replace(data, "night")
					newfile += line + "\n"
			settings.close()
			new_settings = open("/home/billy/Desktop/camera/camera_settings.txt", "w")
			new_settings.write(newfile)
			new_settings.close()
			menu(screen)
		if GPIO.input(select) == GPIO.LOW and opt == 4:
			time.sleep(.5)
			newfile = ""
			with open("/home/billy/Desktop/camera/camera_settings.txt", "r") as settings:
				for line in settings:
					if "exposure" in line:
						data = line.split()[1]
						line = line.replace(data, "snow")
					newfile += line + "\n"
			settings.close()
			new_settings = open("/home/billy/Desktop/camera/camera_settings.txt", "w")
			new_settings.write(newfile)
			new_settings.close()
			menu(screen)
		if GPIO.input(select) == GPIO.LOW and opt == 5:
			time.sleep(.5)
			newfile = ""
			with open("/home/billy/Desktop/camera/camera_settings.txt", "r") as settings:
				for line in settings:
					if "exposure" in line:
						data = line.split()[1]
						line = line.replace(data, "beach")
					newfile += line + "\n"
			settings.close()
			new_settings = open("/home/billy/Desktop/camera/camera_settings.txt", "w")
			new_settings.write(newfile)
			new_settings.close()
			menu(screen)
		if GPIO.input(select) == GPIO.LOW and opt == 6:
			time.sleep(.5)
			newfile = ""
			with open("/home/billy/Desktop/camera/camera_settings.txt", "r") as settings:
				for line in settings:
					if "exposure" in line:
						data = line.split()[1]
						line = line.replace(data, "antishake")
					newfile += line + "\n"
			settings.close()
			new_settings = open("/home/billy/Desktop/camera/camera_settings.txt", "w")
			new_settings.write(newfile)
			new_settings.close()
			menu(screen)
		
		pygame.display.flip()

# White balance is used to adjust colors to match the color of the 
# light source so that white objects appear white
# default is set to auto
def white_balance(screen):
	
	opt = 1
	row = 50
	time.sleep(.5)
	while 1:
		screen.fill(BLACK)
		font = pygame.font.SysFont(None, 30)
		menu_list1 = font.render('White Balance', True, WHITE)
		menu_list2 = font.render('auto', True, WHITE)
		menu_list3 = font.render('off', True, WHITE)
		menu_list4 = font.render('sunlight', True, WHITE)
		menu_list5 = font.render('cloudy', True, WHITE)
		menu_list6 = font.render('fluorescent', True, WHITE)
		menu_list7 = font.render('flash', True, WHITE)
		screen.blit(menu_list1, (60, 20))
		screen.blit(menu_list2, (60, 45))
		screen.blit(menu_list3, (60, 70))
		screen.blit(menu_list4, (60, 95))
		screen.blit(menu_list5, (60, 120))
		screen.blit(menu_list6, (60, 145))
		screen.blit(menu_list7, (60, 170))
		
		
		# up button selection
		if GPIO.input(up) == GPIO.LOW and opt == 1:
			time.sleep(.5)
			opt = 2
			row = 75
		if GPIO.input(up) == GPIO.LOW and opt == 2:
			time.sleep(.5)
			opt = 3
			row = 100
		if GPIO.input(up) == GPIO.LOW and opt == 3:
			time.sleep(.5)
			opt = 4
			row = 125
		if GPIO.input(up) == GPIO.LOW and opt == 4:
			time.sleep(.5)
			opt = 5
			row = 150
		if GPIO.input(up) == GPIO.LOW and opt == 5:
			time.sleep(.5)
			opt = 6
			row = 175
		if GPIO.input(up) == GPIO.LOW and opt == 6:
			time.sleep(.5)
			opt = 1
			row = 50
		
		# down button selection
		if GPIO.input(down) == GPIO.LOW and opt == 1:
			time.sleep(.5)
			opt = 6
			row = 175
		if GPIO.input(down) == GPIO.LOW and opt == 2:
			time.sleep(.5)
			opt = 1
			row = 50
		if GPIO.input(down) == GPIO.LOW and opt == 3:
			time.sleep(.5)
			opt = 2
			row = 75
		if GPIO.input(down) == GPIO.LOW and opt == 4:
			time.sleep(.5)
			opt = 3
			row = 100
		if GPIO.input(down) == GPIO.LOW and opt == 5:
			time.sleep(.5)
			opt = 4
			row = 125
		if GPIO.input(down) == GPIO.LOW and opt == 6:
			time.sleep(.5)
			opt = 5
			row = 150

		pygame.draw.rect(screen, RED, pygame.Rect(350, row, 20, 20))

		# select key pressed
		if GPIO.input(select) == GPIO.LOW and opt == 1:
			time.sleep(.5)
			newfile = ""
			with open("/home/billy/Desktop/camera/camera_settings.txt", "r") as settings:
				for line in settings:
					if "white" in line:
						data = line.split()[1]
						line = line.replace(data, "auto")
					newfile += line + "\n"
			settings.close()
			new_settings = open("/home/billy/Desktop/camera/camera_settings.txt", "w")
			new_settings.write(newfile)
			new_settings.close()
			menu(screen)
		if GPIO.input(select) == GPIO.LOW and opt == 2:
			time.sleep(.5)
			newfile = ""
			with open("/home/billy/Desktop/camera/camera_settings.txt", "r") as settings:
				for line in settings:
					if "white" in line:
						data = line.split()[1]
						line = line.replace(data, "off")
					newfile += line + "\n"
			settings.close()
			new_settings = open("/home/billy/Desktop/camera/camera_settings.txt", "w")
			new_settings.write(newfile)
			new_settings.close()
			menu(screen)
		if GPIO.input(select) == GPIO.LOW and opt == 3:
			time.sleep(.5)
			newfile = ""
			with open("/home/billy/Desktop/camera/camera_settings.txt", "r") as settings:
				for line in settings:
					if "white" in line:
						data = line.split()[1]
						line = line.replace(data, "sunlight")
					newfile += line + "\n"
			settings.close()
			new_settings = open("/home/billy/Desktop/camera/camera_settings.txt", "w")
			new_settings.write(newfile)
			new_settings.close()
			menu(screen)
		if GPIO.input(select) == GPIO.LOW and opt == 4:
			time.sleep(.5)
			newfile = ""
			with open("/home/billy/Desktop/camera/camera_settings.txt", "r") as settings:
				for line in settings:
					if "white" in line:
						data = line.split()[1]
						line = line.replace(data, "cloudy")
					newfile += line + "\n"
			settings.close()
			new_settings = open("/home/billy/Desktop/camera/camera_settings.txt", "w")
			new_settings.write(newfile)
			new_settings.close()
			menu(screen)
		if GPIO.input(select) == GPIO.LOW and opt == 5:
			time.sleep(.5)
			newfile = ""
			with open("/home/billy/Desktop/camera/camera_settings.txt", "r") as settings:
				for line in settings:
					if "white" in line:
						data = line.split()[1]
						line = line.replace(data, "fluorescent")
					newfile += line + "\n"
			settings.close()
			new_settings = open("/home/billy/Desktop/camera/camera_settings.txt", "w")
			new_settings.write(newfile)
			new_settings.close()
			menu(screen)
		if GPIO.input(select) == GPIO.LOW and opt == 6:
			time.sleep(.5)
			newfile = ""
			with open("/home/billy/Desktop/camera/camera_settings.txt", "r") as settings:
				for line in settings:
					if "white" in line:
						data = line.split()[1]
						line = line.replace(data, "flash")
					newfile += line + "\n"
			settings.close()
			new_settings = open("/home/billy/Desktop/camera/camera_settings.txt", "w")
			new_settings.write(newfile)
			new_settings.close()
			menu(screen)
		
		pygame.display.flip()


# this is used to add effects to images
# default is none
def effects(screen):

	opt = 1
	row = 50
	time.sleep(.5)
	while 1:
		screen.fill(BLACK)
		font = pygame.font.SysFont(None, 30)
		menu_list1 = font.render('Image Effects', True, WHITE)
		menu_list2 = font.render('none', True, WHITE)
		menu_list3 = font.render('negative', True, WHITE)
		menu_list4 = font.render('colour swap', True, WHITE)
		menu_list5 = font.render('cartoon', True, WHITE)
		menu_list6 = font.render('sketch', True, WHITE)
		menu_list7 = font.render('oilpaint', True, WHITE)
		screen.blit(menu_list1, (60, 20))
		screen.blit(menu_list2, (60, 45))
		screen.blit(menu_list3, (60, 70))
		screen.blit(menu_list4, (60, 95))
		screen.blit(menu_list5, (60, 120))
		screen.blit(menu_list6, (60, 145))
		screen.blit(menu_list7, (60, 170))
		
		# up button selection
		if GPIO.input(up) == GPIO.LOW and opt == 1:
			time.sleep(.5)
			opt = 2
			row = 75
		if GPIO.input(up) == GPIO.LOW and opt == 2:
			time.sleep(.5)
			opt = 3
			row = 100
		if GPIO.input(up) == GPIO.LOW and opt == 3:
			time.sleep(.5)
			opt = 4
			row = 125
		if GPIO.input(up) == GPIO.LOW and opt == 4:
			time.sleep(.5)
			opt = 5
			row = 150
		if GPIO.input(up) == GPIO.LOW and opt == 5:
			time.sleep(.5)
			opt = 6
			row = 175
		if GPIO.input(up) == GPIO.LOW and opt == 6:
			time.sleep(.5)
			opt = 1
			row = 50
		
		# down button selection
		if GPIO.input(down) == GPIO.LOW and opt == 1:
			time.sleep(.5)
			opt = 6
			row = 175
		if GPIO.input(down) == GPIO.LOW and opt == 2:
			time.sleep(.5)
			opt = 1
			row = 50
		if GPIO.input(down) == GPIO.LOW and opt == 3:
			time.sleep(.5)
			opt = 2
			row = 75
		if GPIO.input(down) == GPIO.LOW and opt == 4:
			time.sleep(.5)
			opt = 3
			row = 100
		if GPIO.input(down) == GPIO.LOW and opt == 5:
			time.sleep(.5)
			opt = 4
			row = 125
		if GPIO.input(down) == GPIO.LOW and opt == 6:
			time.sleep(.5)
			opt = 5
			row = 150

		pygame.draw.rect(screen, RED, pygame.Rect(350, row, 20, 20))

		# select key pressed
		if GPIO.input(select) == GPIO.LOW and opt == 1:
			time.sleep(.5)
			newfile = ""
			with open("/home/billy/Desktop/camera/camera_settings.txt", "r") as settings:
				for line in settings:
					if "effect" in line:
						data = line.split()[1]
						line = line.replace(data, "none")
					newfile += line + "\n"
			settings.close()
			new_settings = open("/home/billy/Desktop/camera/camera_settings.txt", "w")
			new_settings.write(newfile)
			new_settings.close()
			menu(screen)
		if GPIO.input(select) == GPIO.LOW and opt == 2:
			time.sleep(.5)
			newfile = ""
			with open("/home/billy/Desktop/camera/camera_settings.txt", "r") as settings:
				for line in settings:
					if "effect" in line:
						data = line.split()[1]
						line = line.replace(data, "negative")
					newfile += line + "\n"
			settings.close()
			new_settings = open("/home/billy/Desktop/camera/camera_settings.txt", "w")
			new_settings.write(newfile)
			new_settings.close()
			menu(screen)
		if GPIO.input(select) == GPIO.LOW and opt == 3:
			time.sleep(.5)
			newfile = ""
			with open("/home/billy/Desktop/camera/camera_settings.txt", "r") as settings:
				for line in settings:
					if "effect" in line:
						data = line.split()[1]
						line = line.replace(data, "colorswap")
					newfile += line + "\n"
			settings.close()
			new_settings = open("/home/billy/Desktop/camera/camera_settings.txt", "w")
			new_settings.write(newfile)
			new_settings.close()
			menu(screen)
		if GPIO.input(select) == GPIO.LOW and opt == 4:
			time.sleep(.5)
			newfile = ""
			with open("/home/billy/Desktop/camera/camera_settings.txt", "r") as settings:
				for line in settings:
					if "effect" in line:
						data = line.split()[1]
						line = line.replace(data, "cartoon")
					newfile += line + "\n"
			settings.close()
			new_settings = open("/home/billy/Desktop/camera/camera_settings.txt", "w")
			new_settings.write(newfile)
			new_settings.close()
			menu(screen)
		if GPIO.input(select) == GPIO.LOW and opt == 5:
			time.sleep(.5)
			newfile = ""
			with open("/home/billy/Desktop/camera/camera_settings.txt", "r") as settings:
				for line in settings:
					if "effect" in line:
						data = line.split()[1]
						line = line.replace(data, "sketch")
					newfile += line + "\n"
			settings.close()
			new_settings = open("/home/billy/Desktop/camera/camera_settings.txt", "w")
			new_settings.write(newfile)
			new_settings.close()
			menu(screen)
		if GPIO.input(select) == GPIO.LOW and opt == 6:
			time.sleep(.5)
			newfile = ""
			with open("/home/billy/Desktop/camera/camera_settings.txt", "r") as settings:
				for line in settings:
					if "effect" in line:
						data = line.split()[1]
						line = line.replace(data, "oilpaint")
					newfile += line + "\n"
			settings.close()
			new_settings = open("/home/billy/Desktop/camera/camera_settings.txt", "w")
			new_settings.write(newfile)
			new_settings.close()
			menu(screen)
		
		pygame.display.flip()

def picview(screen):

	time.sleep(.5)
	screen.fill(BLACK)

	font = pygame.font.SysFont(None, 30)
	menu_list1 = font.render('Press UP or DOWN to view different images', True, WHITE)
	menu_list2 = font.render('Press SELECT to exit', True, WHITE)
	screen.blit(menu_list1, (20, 20))
	screen.blit(menu_list2, (20, 45))

	path = "/home/billy/Desktop/photos/"
	file_list = os.listdir(path)

	filename = os.path.join("/home/billy/Desktop/photos/", file_list[0])

	image1 = pygame.image.load(filename)

	screen.blit(image1,(20,70))

	y = len(file_list)
	print(str(y))
	x = 0

	while(1):
			
		print(str(x))
		if GPIO.input(up) == GPIO.LOW:
			time.sleep(2)
			x = x + 1
			if x > y - 1:
				x = 0
		
		# down button selection
		if GPIO.input(down) == GPIO.LOW:
			time.sleep(2)
			x = x - 1
			if x < 0:
				x = y - 1

		if GPIO.input(select) == GPIO.LOW:
			time.sleep(.5)
			menu(screen)

		filename = os.path.join("/home/billy/Desktop/photos/", file_list[x])
		image1 = pygame.image.load(filename)
		screen.blit(image1,(20,70))

		pygame.display.flip()

def main():

	# text file variables
	mode = 0
	bright = 0
	cont = 0
	expo = ''
	white = ''
	effect = ''

	camera = PiCamera()
	camera.resolution = (2592, 1944)
	camera.framerate = 15
	# start camera preview on startup - 
	camera.start_preview(fullscreen=True)
	time.sleep(.5)

	pygame.init()
	# Set the height and width of the screen
	size = [SCREEN_WIDTH, SCREEN_HEIGHT]
	# set up the screen and its size
	screen = pygame.display.set_mode(size)
	pygame.mouse.set_visible(False)
	
	# Loop until the user clicks the close button.
	done = False
	# Used to manage how fast the screen updates
	clock = pygame.time.Clock()

	# settings text file
	# change directory to something appropiate on the pi
	with open("/home/billy/Desktop/camera/camera_settings.txt", "r") as settings:
		for line in settings:
			#print(line)
			if "mode" in line:
				mode = int(line.split()[1])
			if "brightness" in line:
				bright = line.split()[1]
			if "contrast" in line:
				cont = line.split()[1]
			if "exposure" in line:
				expo = line.split()[1]
			if "white" in line:
				white = line.split()[1]
			if "effect" in line:
				effect = line.split()[1]

	settings.close()

	# apply the settings
	camera.brightness = int(bright)
	camera.contrast = int(cont)
	camera.exposure_mode = expo
	camera.awb_mode = white
	camera.image_effect = effect


	while not done:
		# Event Processing to quit
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				done = True

		if GPIO.input(snap) == GPIO.LOW:
			time.sleep(.5)
			# mode 1 = take single photo
			if mode == 1:
				# Returns a datetime object containing the local date and time
				now = datetime.now()
				# get the time object from datetime object
				timevar = str(now.strftime("%H%M%S"))
				pathstring = timevar + ".jpg"
				filename = os.path.join("/home/billy/Desktop/photos/", pathstring)
				camera.capture(filename)
			
			# mode 2 = 5 burst, 250ms in between
			if mode == 2:
				for i in range(6):
					# Returns a datetime object containing the local date and time
					now = datetime.now()
					# get the time object from datetime object
					timevar = str(now.strftime("%H%M%S"))
					pathstring = timevar + ".jpg"
					filename = os.path.join("/home/billy/Desktop/photos/", pathstring)
					camera.capture(filename)
					time.sleep(.25)
				
			# mode 3 = video
			if mode == 3:
				
				VIDEO_WIDTH = 1920
				VIDEO_HEIGHT = 1080

				# max resolution for video is 1920x1080
				camera.resolution = (VIDEO_WIDTH, VIDEO_HEIGHT)
				camera.framerate = 30

				now = datetime.now()
				timevar = str(now.strftime("%H%M%S"))
				pathstring = timevar + ".h264"
				mp4pathstring = timevar + ".mp4"
				filename = os.path.join("/home/billy/Desktop/videos/", pathstring)
				mp4filename = os.path.join("/home/billy/Desktop/videos/", mp4pathstring)
				camera.start_recording(filename)

				img = Image.open('/home/billy/Desktop/camera/rec.png')
				pad = Image.new('RGB', (((img.size[0] + 31) // 32) * 32,((img.size[1] + 15) // 16) * 16,))
				pad.paste(img, (0, 0))
				o = camera.add_overlay(pad.tobytes(), size=img.size)
				o.alpha = 50
				o.layer = 3
								

				start = time.time()
				time.sleep(1)
				while time.time() - start < 300 and GPIO.input(snap) == True: 				
					
					time.sleep(.1)
				
				camera.remove_overlay(o)
				camera.stop_recording()	
				time.sleep(3)
				camera.resolution = (2592, 1944)
				# convert video format to MP4 using bash command and MP4Box
				# 1 set up the command to send to bash shell
				commandstring = "MP4Box -add " + filename + " " + mp4filename
				# 2 send the command to shell
				subprocess.run(shlex.split(commandstring))
				# remove the original file as it is no longer required
				os.remove(filename)

				

		if GPIO.input(select) == GPIO.LOW:
			time.sleep(.5)
			camera.stop_preview()
			camera.close()
			menu(screen)

		# Limit to 60 frames per second
		clock.tick(60)

		# Go ahead and update the screen with what we've drawn.
		pygame.display.flip()

	# Close everything down
	pygame.quit()


if __name__ == "__main__":
	main()	