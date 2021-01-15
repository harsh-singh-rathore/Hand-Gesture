import numpy as np
import cv2 as cv
import imutils


def skinmask(img, kernel_size = 3):
    """
    Function takes in input the image and kernel size for the blurring and returns the masked image where skin colour is masked
    img -> image to mask
    kernel_size -> size of the kernel to blur
    returns
    thresh -> masked image
    """
    hsvim = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    lower = np.array([0, 48, 80], dtype = "uint8")
    upper = np.array([20, 255, 255], dtype = "uint8")
    skinRegionHSV = cv.inRange(hsvim, lower, upper)
    blurred = cv.blur(skinRegionHSV, (kernel_size,kernel_size))
    mask = cv.dilate(blurred,kernel = np.ones((kernel_size, kernel_size),np.uint8),iterations = 4)
    ret, thresh = cv.threshold(mask,0,255,cv.THRESH_BINARY)
    return thresh


def getcnthull(mask_img):
    """
    Function takes in imput a masked image and returns the contour of largest area and it's convex hull
    mask_img -> maked image/ thresholded image
    return 
    contours -> contour of the largest area
    hull -> convex hull of the largest area
    """
    contours, hierarchy = cv.findContours(mask_img, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    contours = max(contours, key=lambda x: cv.contourArea(x))
    hull = cv.convexHull(contours)
    return contours, hull

def getdefects(contours):
    """
    Function returns the convexity defects in the contours with the help of which we will be calculate the number of fingers
    contours -> takes in the contours in the image
    returns
    defects -> convexity defects in the image
    """
    hull = cv.convexHull(contours, returnPoints=False)
    defects = cv.convexityDefects(contours, hull)
    return defects



# Image processing 
def imageProcessing(frame : np.ndarray, roiSize : dict, font, line_type):
    # define ROI 
    x = roiSize['x']
    y = roiSize['y']
    l = roiSize['l']
    w = roiSize['w']
    kernelSize = roiSize['dialationKernelSize']

    roi = frame[y:y+w, x:x+l]
    cv.rectangle(frame, (x,y),(x+l,y+w),(0,255,0),3)
    mask_img = roi
    try:
        mask_img = skinmask(roi, kernelSize)
        contours, hull = getcnthull(mask_img)
        cv.drawContours(roi, [contours], -1, (255,255,0), 2)
        cv.drawContours(roi, [hull], -1, (0, 255, 255), 2)
        defects = getdefects(contours)
        if defects is not None:
            cnt = 0
            for i in range(defects.shape[0]):  # calculate the angle
                s, e, f, d = defects[i][0]
                start = tuple(contours[s][0])
                end = tuple(contours[e][0])
                far = tuple(contours[f][0])
                a = np.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
                b = np.sqrt((far[0] - start[0]) ** 2 + (far[1] - start[1]) ** 2)
                c = np.sqrt((end[0] - far[0]) ** 2 + (end[1] - far[1]) ** 2)
                angle = np.arccos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c))  #      cosine theorem
                if angle <= np.pi / 2:  # angle less than 90 degree, treat as fingers
                    cnt += 1
                    cv.circle(roi, far, 4, [0, 0, 255], -1)
            if cnt > 0 and cnt < 5:
                cnt = cnt+1
                cv.putText(frame, str(cnt), (0, 50), font,1, (255, 0, 0) , 2, line_type)
            else:
                cv.putText(frame, "Place the hand correctly in the green box", (0, 50), font,1, (255, 0, 0) , 2, line_type)
    except:
        pass
    return frame, mask_img



def main():
    imageProcessing