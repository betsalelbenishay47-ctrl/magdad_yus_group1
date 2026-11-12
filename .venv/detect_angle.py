import cv2
import math
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.pyplot as plt
import copy

def detect_line(img):
    """
    :param
    :return: x, y: int, int
    """
    def nothing(x):
        pass

    import cv2
    import numpy as np

    # Load image in grayscale
    kernel_size = 17
    blur_img = cv2.GaussianBlur(img, (kernel_size, kernel_size), 0)



    # Apply Sobel operator
    sobelx = cv2.Sobel(blur_img, cv2.CV_64F, 1, 0, ksize=3)  # Horizontal edges
    sobely = cv2.Sobel(blur_img, cv2.CV_64F, 0, 1, ksize=3)  # Vertical edges

    # Compute gradient magnitude
    gradient_magnitude = cv2.magnitude(sobelx, sobely)

    # Convert to uint8
    gradient_magnitude = cv2.convertScaleAbs(gradient_magnitude)

    # Display result

    #cv2.imshow("Sobel Edge Detection", gradient_magnitude)
    #cv2.waitKey(0)
    kernel_size = 15
    blur_gray = cv2.GaussianBlur(gradient_magnitude, (kernel_size, kernel_size), 0)
    low_threshold = 80
    high_threshold = 150
    edges = cv2.Canny(blur_gray, low_threshold, high_threshold)
    #cv2.imshow("Edge Detection", edges)
    #cv2.waitKey(0)
    rho = 1  # distance resolution in pixels of the Hough grid
    theta = np.pi / 180  # angular resolution in radians of the Hough grid
    threshold = 15  # minimum number of votes (intersections in Hough grid cell)
    min_line_length = 50  # minimum number of pixels making up a line
    max_line_gap = 20  # maximum gap in pixels between connectable line segments
    line_image = np.copy(img) * 0  # creating a blank to draw lines on

    # Run Hough on edge detected image
    # Output "lines" is an array containing endpoints of detected line segments
    lines = cv2.HoughLinesP(edges, rho, theta, threshold, np.array([]),
                            min_line_length, max_line_gap)

    try:
        for line in lines:
            cv2.line(line_image, (line[0], line[1]), (line[2], line[3]), (255, 0, 0), 3)
        lines_edges = cv2.addWeighted(img, 0.8, line_image, 1, 0)
        cv2.destroyAllWindows()
        return lines
    except:
        return []

def detect_intersection_of_lines(lines):

    def line_intersection(line1, line2):
        line11 = line1
        line12 = line2
        line1 = [[line1[0], line1[1]], [line1[2], line1[3]]]
        line2 = [[line2[0], line2[1]], [line2[2], line2[3]]]
        xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
        ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

        def det(a, b):
            return a[0] * b[1] - a[1] * b[0]

        div = det(xdiff, ydiff)
        if div == 0:
            return 0, 0

        d = (det(*line1), det(*line2))
        x = det(d, xdiff) / div
        y = det(d, ydiff) / div
        error = 20  # what is the error of how much lines are far away.


        if x < min(line11[0], line11[2]) - error or x > max(line11[2], line11[0]) + error:
            return 0, 0
        if y < min(line12[1], line12[3]) - error or y > max(line12[3], line12[1])+ error:
            return 0, 0
        if x < min(line12[0], line12[2]) - error or x > max(line12[2], line12[0]) + error:
            return 0, 0
        if y < min(line12[1], line12[3]) - error or y > max(line12[3], line12[1]) + error:
            return 0, 0
        return x, y


    point_of_angle = []
    for i in range(len(lines)):
        for j in range(i,len(lines)):
            if line_intersection(lines[i], lines[j])[0] != 0:
                point_of_angle.append(line_intersection(lines[i], lines[j]))
    return point_of_angle




def point_angle(img):
    for p in detect_intersection_of_lines(detect_line(img)):
        if p[0] != 0:
            cv2.circle(img, center=(int(p[0]), int(p[1])), radius=3, color=(0, 255, 0), thickness=4)
    return img

#img = cv2.imread('123.png', cv2.IMREAD_GRAYSCALE)
#point_angle(img)
