import cv2
import math
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
from detect_angle import *
import copy

def mask_black(image):
    image1 = np.copy(image)

    # Convert Image to Image HSV
    hsv = cv2.cvtColor(image1, cv2.COLOR_BGR2HSV)

    # Defining lower and upper bound HSV values
    lower = np.array([0, 0, 0])
    upper = np.array([360,255,90])



    # Defining mask for detecting color
    mask = cv2.inRange(hsv, lower, upper)
    # Display Image and Mask


    return mask

def detect_usb_entier(image):
    gradient_magnitude = mask_black(image)

    contours, _ = cv2.findContours(gradient_magnitude, cv2.RETR_TREE,
                                   cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        area = cv2.contourArea(cnt)

        # Shortlisting the regions based on there area.
        if area > 1000 and area < 10000:
            approx = cv2.approxPolyDP(cnt,
                                      0.009 * cv2.arcLength(cnt, True), True)
            print(approx)
            print("x")

            # Checking if the no. of sides of the selected region is 7.
            if (len(approx) >= 3) and (len(approx) <= 9):
                cv2.drawContours(image1, [approx], 0, (0, 0, 255), 10)

    # Display result
    cv2.imshow("Sobel Edge Detection", gradient_magnitude)
    cv2.waitKey(0)

image1 = cv2.imread("212.png")
detect_usb_entier(image1)
cv2.imshow("Sobel Edge Detection", image1)
cv2.waitKey(0)
