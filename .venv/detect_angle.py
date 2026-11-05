import cv2
import math
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.pyplot as plt
import copy

def detect_angle(image):
    """
    the function cut rect from picture and return image
    :param image: list[int]
    :param x1:int
    :param y1:int
    :param x2:int
    :param y2:int
    :return: list[list[list]]]
    """
    # Reading image
    img2 = copy.deepcopy(image)

    # Reading same image in another variable and
    # converting to gray scale.

    img = copy.deepcopy(image)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Converting image to a binary image
    # (black and white only image).

    _, threshold = cv2.threshold(img, 70, 255,
                                 cv2.THRESH_BINARY)
    # cv2.imshow('image2', threshold)
    blurred = cv2.GaussianBlur(threshold, (3, 3), 0)
    cv2.imshow('image2', blurred)

    # Exiting the window if 'q' is pressed on the keyboard.
    if cv2.waitKey(0) & 0xFF == ord('q'):
        cv2.destroyAllWindows()

    # Detecting shapes in image by selecting region
    # with same colors or intensity.
    contours, _ = cv2.findContours(blurred, cv2.RETR_TREE,
                                   cv2.CHAIN_APPROX_SIMPLE)
    edged = cv2.Canny(blurred, 50, 100)
    cv2.imshow("Image", edged)
    cv2.waitKey(0)

    # Searching through every region selected to
    # find the required polygon.
    for cnt in contours:
        area = cv2.contourArea(cnt)

        # Shortlisting the regions based on there area.
        if area > 600:
            approx = cv2.approxPolyDP(cnt,
                                      0.009 * cv2.arcLength(cnt, True), True)
            print(approx)
            print("x")

            # Checking if the no. of sides of the selected region is 7.
            if (len(approx) >= 3) and (len(approx) <= 9):
                cv2.drawContours(img2, [approx], 0, (0, 0, 255), 10)

    # Showing the image along with outlined arrow.
    cv2.imshow('image2', img2)

    # Exiting the window if 'q' is pressed on the keyboard.
    if cv2.waitKey(0) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
    crop_img = img[y1:y2, x1:x2]
    return crop_img