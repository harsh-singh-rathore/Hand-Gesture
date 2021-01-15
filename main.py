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
    "x": 400,
    "y": 100,
    "l": 200,
    "w": 300,
    "dialationKernelSize": 3
}
####################################




def main():
    videoCamera(0, textFormat, roiSize)
    exit()
    

if __name__ == '__main__':
    main()