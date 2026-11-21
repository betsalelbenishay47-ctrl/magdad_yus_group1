import cv2
import math
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.pyplot as plt
import copy

def detect_edges(img):
    # Load image in grayscale
    kernel_size = 15
    blur_img = cv2.GaussianBlur(img, (kernel_size, kernel_size), 0)

    # Apply Sobel operator
    sobelx = cv2.Sobel(blur_img, cv2.CV_64F, 1, 0, ksize=3)  # Horizontal edges
    sobely = cv2.Sobel(blur_img, cv2.CV_64F, 0, 1, ksize=3)  # Vertical edges

    # Compute gradient magnitude
    gradient_magnitude = cv2.magnitude(sobelx, sobely)

    # Convert to uint8
    gradient_magnitude = cv2.convertScaleAbs(gradient_magnitude)

    # Display result
    # cv2.imshow("Sobel Edge Detection", gradient_magnitude)
    # cv2.waitKey(0)

    gradient_magnitude = cv2.convertScaleAbs(gradient_magnitude)
    return gradient_magnitude

def detect_line(img):
    """
    the goal of this function is to detect line espcialy the frame of the computer.
    :param
    :return: x, y: int, int
    """
    def nothing(x):
        pass



    # Load image in grayscale
    kernel_size = 15
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

    gradient_magnitude = cv2.convertScaleAbs(gradient_magnitude)
    kernel_size = 5
    low_threshold = 70
    high_threshold = 150
    blur_gray = cv2.GaussianBlur(gradient_magnitude, (kernel_size, kernel_size), 0)
    edges = cv2.Canny(blur_gray, low_threshold, high_threshold)
    cv2.imshow("Edge Detection", edges)
    cv2.waitKey(1)

    rho = 1 # distance resolution in pixels of the Hough grid
    theta = np.pi / 180  # angular resolution in radians of the Hough grid
    threshold = 15  # minimum number of votes (intersections in Hough grid cell)
    min_line_length = 50  # minimum number of pixels making up a line
    max_line_gap = 15  # maximum gap in pixels between connectable line segments
    line_image = np.copy(img) * 0  # creating a blank to draw lines on

    # Run Hough on edge detected image
    # Output "lines" is an array containing endpoints of detected line segments
    lines = cv2.HoughLinesP(edges, rho, theta, threshold, np.array([]),
                            min_line_length, max_line_gap)

    try:
        for line in lines:
            cv2.line(line_image, (line[0], line[1]), (line[2], line[3]), (255, 0, 0), 3)# draw line at the picture


        lines_edges = cv2.addWeighted(img, 0.8, line_image, 1, 0)
        
        return lines, pass_only_blue_color(line_image)
    except:
        return [], pass_only_blue_color(line_image)


def pass_only_blue_color(img):
    image = np.copy(img)

    # Convert Image to Image HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Defining lower and upper bound HSV values
    lower = np.array([110, 100, 100])
    upper = np.array([130, 255, 255])
    # Get green color
    green = np.uint8([[[255, 0, 0]]])


    # Defining mask for detecting color
    mask = cv2.inRange(hsv, lower, upper)
    # Display Image and Mask

    return mask


def detect_intersection_of_lines(lines):
    """
    the goal of this function is to detect intersection of lines for detcet corner
    but this function don't work for our system.
    :param lines:
    :return: 2 point
    """

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
        error = 0  # what is the error of how much lines are far away.


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




def point_angle_with_interction_of_line(img):
    for p in detect_intersection_of_lines(detect_line(img)[0]):
        if p[0] != 0:
            cv2.circle(img, center=(int(p[0]), int(p[1])), radius=3, color=(0, 0, 255), thickness=4)
    return img

"""
img = cv2.imread('123.png', cv2.IMREAD_GRAYSCALE)
point_angle(img)
cv2.imshow('img', img)
cv2.waitKey(0)
"""
def detect_corners(img):
    """
    this function use function from cv to slove this problem but for our problem it iswnt work
    :param img:
    :return:
    """
    import numpy as np
    import cv2 as cv
    img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)


    kernel_size = 11
    blur_img = cv2.GaussianBlur(img_gray, (kernel_size, kernel_size), 0)

    # Apply Sobel operator
    sobelx = cv2.Sobel(blur_img, cv2.CV_64F, 1, 0, ksize=3)  # Horizontal edges
    sobely = cv2.Sobel(blur_img, cv2.CV_64F, 0, 1, ksize=3)  # Vertical edges

    # Compute gradient magnitude
    gradient_magnitude = cv2.magnitude(sobelx, sobely)

    # Convert to uint8
    gradient_magnitude = cv2.convertScaleAbs(gradient_magnitude)
    kernel_size = 5
    low_threshold = 70
    high_threshold = 150
    blur_gray = cv2.GaussianBlur(gradient_magnitude, (kernel_size, kernel_size), 0)
    edges = cv2.Canny(blur_gray, low_threshold, high_threshold)

    rho = 1  # distance resolution in pixels of the Hough grid
    theta = np.pi / 180  # angular resolution in radians of the Hough grid
    threshold = 15  # minimum number of votes (intersections in Hough grid cell)
    min_line_length = 50  # minimum number of pixels making up a line
    max_line_gap = 30  # maximum gap in pixels between connectable line segments
    line_image = np.copy(img) * 0  # creating a blank to draw lines on

    # Run Hough on edge detected image
    # Output "lines" is an array containing endpoints of detected line segments
    lines = cv2.HoughLinesP(edges, rho, theta, threshold, np.array([]),
                            min_line_length, max_line_gap)
    try:
        for line in lines:
            cv2.line(line_image, (line[0], line[1]), (line[2], line[3]), (255, 0, 0), 3)
            cv2.circle(img, (line[0], line[1]), radius=3, color=(255, 0, 255), thickness=-1)
        lines_edges = cv2.addWeighted(img, 0.8, line_image, 1, 0)
    except:
        pass
    
    cv2.imshow('edges', edges)
    gray = blur_gray
    gray = np.float32(gray)
    corners = cv2.goodFeaturesToTrack(
        gray,
        maxCorners=5,
        qualityLevel=0.01,
        minDistance=5,
        blockSize=5,
        useHarrisDetector=False,
        k=0.04
    )
    corners = np.intp(corners)  # Convert to integer coords
    for corner in corners:
        x, y = corner.ravel()
        valid_corner = 0
        for corner2 in corners:
            x2, y2 = corner2.ravel()
            if abs(x2 - x)**2 + abs(y2 - y)**2 < 50 and (x != x2 or y != y2):
                valid_corner += 1
        if valid_corner > 0:        
            cv2.circle(img, (x, y), radius=3, color=(0, 255, 0), thickness=-1)


    return img



def d(line):
    return np.sqrt(abs(line[0] - line[2])**2 + abs(line[1] - line[3])**2)



def max_line(lines):
    max_length = 0
    max_length_line = [0,0,0,0]
    for line in lines:
        if d(line) > max_length:
            max_length = d(line)
            max_length_line = line
    return max_length_line


def detect_up_corner_computer(img):
    """
    this function draw line at the top of frame of computer and after that find the corner with the edges of the drawing.
    :param img: list[list[lsit[int]]]
    :return: (int,int), (int,int)
    """
    up_edge_suspect = detect_line(img)[1]

    rho = 1  # distance resolution in pixels of the Hough grid
    theta = np.pi / 180  # angular resolution in radians of the Hough grid
    threshold = 15  # minimum number of votes (intersections in Hough grid cell)
    min_line_length = 30  # minimum number of pixels making up a line
    max_line_gap = 10  # maximum gap in pixels between connectable line segments
    line_image = np.copy(img) * 0  # creating a blank to draw lines on

    # Run Hough on edge detected image
    # Output "lines" is an array containing endpoints of detected line segments
    lines = cv2.HoughLinesP(up_edge_suspect, rho, theta, threshold, np.array([]),
                            min_line_length, max_line_gap)


    try:
        max_length_line = max_line(lines)
        print(max_length_line)
        cv2.line(up_edge_suspect, (max_length_line[0], max_length_line[1]),(max_length_line[2], max_length_line[3]), (0, 255, 0), 2)
        print("x")
        print((max_length_line[3] - max_length_line[1])/(max_length_line[0]-max_length_line[2]))
        WE_WANT_SEE_WAY = True
        if WE_WANT_SEE_WAY:
            cv2.imshow("Image", img)
            cv2.imshow("Mask", up_edge_suspect)

            # Make python sleep for unlimited time
            cv2.waitKey(1)

        lines_edges = cv2.addWeighted(img, 0.8, line_image, 1, 0)
    except:
        print("y")
        return (0,0),(0,0)

    return (max_length_line[0], max_length_line[1]), (max_length_line[2], max_length_line[3])


def image_draw_corner_of_computer(img):
    line_max = detect_up_corner_computer(img)
    cv2.circle(img, line_max[0], radius=1, color=(0, 0, 255), thickness=3)
    cv2.circle(img, line_max[1], radius=1, color=(0, 0, 255), thickness=3)







