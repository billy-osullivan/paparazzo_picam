# Paparzzo C/CS 12MP Camera v1.0
# Raspberry pi camera

Raspberry PI HQ camera software for a 4 button GPIO camera
(Dont expect this to be updated with any frequency, but feel free to use the code and change as you want!)

This is a menu driven camera utilizing pygame.
You can view the pictures saved on the camera
To get pictures off of the camera you need to use an FTP client such as filezilla

records pictures and 5 minute max video clips (no audio in this version)

This camera requires 4 GPIO buttons
 
Runs on pygame and python3

Author:			Billy O Sullivan
Created date:		08 June 2022
Edited:			18 August 2022

python 3.10

# 3d files
Available at https://www.printables.com/model/251382-raspberry-pi-camera

# requires MP4Box
sudo apt install -y gpac
enable ssh on the pi to allow you to use SCP to transfer your videos and pictures to your computer

you can change the GPIO pins to whatever you prefer
 
# be sure to change the file paths to what you have on your own raspberry pi

# Directory Layout
I have my directory layout as follows (deviation will require changes to the code!!!)

main directory
/home/billy/Desktop/camera
in here place the camera_settings file
camera python file
rec.png file

/home/billy/Desktop/camera/photos/
your photos are saved here

/home/billy/Desktop/camera/videos/
your videos are saved here

# V1.1 released
This adds support for removing all files to a removable thumb drive
It also adds an option to shut down the camera gracefully 

These options are available in the menu section of the camera gui

