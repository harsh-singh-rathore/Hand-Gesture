from typing import Dict
import numpy as np
import cv2 as cv
import imutils


def videoCamera(cameraNumber : int, textFormat : dict, roiSize : dict):
    cap = cv.VideoCapture(cameraNumber)

    if not cap.isOpened():
        raise Exception("Sorry could not open camera")

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # if frame is read correctly ret is True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break

        # Flip the frame so that the video is normal 
        frame = cv.flip(frame,1)

        font = textFormat['font']
        scale = textFormat['scale']
        thickness = textFormat['thickness']
        linType = textFormat['line type']

        frame = cv.putText(frame, "Press q to exit", (10,25), font, scale, (0,0,255), thickness, linType)

        ###################################################
        # all the function calls are here
        processedImage, frame = imageProcessing(frame, roiSize)
        ###################################################

        # Display the resulting frame
        cv.imshow('frame', frame)
        cv.imshow('roi', processedImage)
        
        # exit at q press
        if cv.waitKey(1) == ord('q'):
            break

    
    # When everything done, release the capture
    cap.release()
    cv.destroyAllWindows()
    
    return



# Image processing 
def imageProcessing(frame : np.ndarray, roiSize : dict):
    # define ROI 
    x = roiSize['x']
    y = roiSize['y']
    l = roiSize['l']
    w = roiSize['w']

    roi = frame[y:y+w, x:x+l]
    cv.rectangle(frame, (x,y),(x+l,y+w),(0,255,0),3)

    return roi, frame


def main():
    textFormat = {
        "font": cv.FONT_HERSHEY_SIMPLEX,
        "scale": 1,
        "line type": cv.LINE_AA,
        "thickness": 2
    }
    roiSize = {
        "x": 300,
        "y": 100,
        "l": 200,
        "w": 300
    }
    videoCamera(0, textFormat, roiSize)
    exit()

if __name__ == "__main__":
    main()