import numpy as np
import cv2 as cv
import imutils

# Function imports 
from getVideo import videoCamera


####################################
# Define all the global variables here
cameraNumber = 0 # change it to the camera number that you want to be used
textFormat = {
    "font": cv.FONT_HERSHEY_SIMPLEX,
    "scale": 1,
    "line type": cv.LINE_AA,
    "thickness": 2
}
roiSize = {
    "x": 100,
    "y": 100,
    "l": 100,
    "w": 100
}
####################################




def main():
    print("hello world")

    videoCamera(cameraNumber= cameraNumber, textFormat)
    

if __name__ == '__main__':
    main()