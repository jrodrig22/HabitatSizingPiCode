#working with a button press

#Installing:
#pi@raspberrypi:~$ sudo apt install python3-gpiozero

#import all necessary libraries
from picamera import PiCamera
import gpiozero
import sys, math
import cv2
import numpy as np
import apriltag
import cv2.aruco as aruco
import RPi.GPIO as io
from time import sleep
from time import strftime
from datetime import datetime
import csv
#initialize some variables
runTime = True
time = float(0)



#Definine the dictionary and parameters.
aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
parameters = aruco.DetectorParameters_create()

#Make the camera.
camera = PiCamera()



#button and led setup
io.setmode(io.BCM)
led1 = 23
io.setup(led1, io.OUT)
io.setup(24, io.IN, pull_up_down=io.PUD_DOWN)

#opens csv file
f = open("results.csv","a")
writer = csv.writer(f)

while runTime == True:
  io.output(led1, True)
  io.wait_for_edge(24, io.RISING)
  
  camera.start_preview()
  sleep(1)
  # Camera warm-up time
  #takes a photo
  camera.capture('/home/pi/Desktop/HabitatSizingStudyPiCode/ssltesting.jpg')
  camera.stop_preview()
  #puts photo in variable for better readability
  imagepathing = '/home/pi/Desktop/HabitatSizingStudyPiCode/ssltesting.jpg'
  #turns photo into grayscale
  src = cv2.imread(imagepathing)
  sslgray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
  #main function to detect the apriltag, corners and rejected are irrelevant (so far)
  corners, ids, rejected = aruco.detectMarkers(sslgray, dictionary = aruco_dict, parameters = parameters)
  
  
  #logs apriltag if it is detected
          
  if ids is not None:
    print(ids)
    
    #visual feedback cue a picture was taken
    for i in range(3):
        io.output(led1, False)
        sleep(1)
        io.output(led1, True)
        sleep(1)
    #gets the date
    now = datetime.now()
    
    timeRec = now.strftime("%H:%M:%S")
    dateRec = now.strftime("%m/%d/%Y")
    #puts id and time into a tuple
    tuple1 = (ids, timeRec, dateRec)
    
    #appends tuple into csv
    writer.writerow(tuple1)
    
    #old write method
    #f.write("{:<8} {:<20}".format(str(ids), str(timeRec)))
    
    #kill program
    if ids==3:
        runTime = False
f.close()
print("Code stopped")
