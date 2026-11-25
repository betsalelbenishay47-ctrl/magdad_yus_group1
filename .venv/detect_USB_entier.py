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
    image = image[250:600 , ]
    gradient_magnitude = mask_black(image)

    contours, _ = cv2.findContours(gradient_magnitude, cv2.RETR_TREE,
                                   cv2.CHAIN_APPROX_SIMPLE)
    x_min = 500
    y_min = 500

    for cnt in contours:
        area = cv2.contourArea(cnt)

        # Shortlisting the regions based on there area.
        if area > 1000:
            approx = cv2.approxPolyDP(cnt,
                                      0.009 * cv2.arcLength(cnt, True), True)
            print(approx)
            for point in approx:
                if point[0][0] < x_min:
                    x_min = point[0][0]
                    y_min = point[0][1]
                    print("x")


            # Checking if the no. of sides of the selected region is 7.
            if (len(approx) >= 3) and (len(approx) <= 13):
                cv2.drawContours(image, [approx], 0, (0, 0, 255), 10)
                print("x")
                cv2.circle(image, (x_min, y_min), radius=3, color=(0, 255, 0), thickness=4)
                print("x")

    # Display result
    cv2.circle(image1, (x_min, y_min), radius=1, color=(0, 255, 0), thickness=3)
    cv2.imshow("Sobel Edge Detection", image)
    cv2.waitKey(0)
    return x_min, y_min


def distance_between_points_x(point1, point2):
    return point1[0] - point2[0]


def distance_between_image(image1, image2):
    point1 = detect_usb_entier(image1)
    point2 = detect_usb_entier(image2)
    return distance_between_points_x(point1, point2)



image1 = cv2.imread("0.png")
image2 = cv2.imread("63.png")
cv2.imshow("Sobel Edge Detection", image1)
cv2.waitKey(0)
print(distance_between_image(image1,image2))
cv2.waitKey(0)

pixel = 410
mm = 65
change_rate = 65/ 410

def distance_to_move_mm(image1, image2):
    return change_rate * distance_between_image(image1, image2)