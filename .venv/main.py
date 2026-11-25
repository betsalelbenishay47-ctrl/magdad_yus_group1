from ultralytics import YOLO
import cv2
import math
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
from detect_angle import *
import copy



def detect_compuet_and_his_angle():
    center = [[],[]]
    edge_x1 = 400
    edge_x2 = 0
    new_edge_x1 = [0, 0]
    new_edge_x2 = [0, 0]
    down_line = 180
    up_line = 20
    # start webcam
    print("x")
    cap = cv2.VideoCapture("120_cm_135.mp4")
    print("x")
    cap.set(3, 640)
    cap.set(4, 480)

    # model
    model = YOLO("yolo26n.pt")

    # object classes
    classNames = ["laptop"
                  ]


    while True:
        success, img = cap.read()
        results = model(img, stream=True)


        # coordinates
        for r in results:

            boxes = r.boxes

            for box in boxes:
                # bounding box
                cls = int(box.cls[0])
                if cls == 63 or cls == 72 or cls == 62:
                    x1, y1, x2, y2 = box.xyxy[0]
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)  # convert to int values
                    down_line = int(abs(0.2*(y1 - y2)))
                    if down_line < 15:
                        down_line = 15

                    # put box in cam
                    cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255),1)  # you are the hashood

                    try:
                        edge_x1, edge_x2 = image_draw_corner_of_computer(img[(y1 - 5):(y1 + down_line), x1:x2], edge_x1, edge_x2)
                        #check if it is only noice
                        if new_edge_x1[0] == edge_x1:
                            new_edge_x1[1] += 1
                            if new_edge_x1[1] >= 20:
                                edge_x1=400
                                new_edge_x1[1] = 0
                        else:
                            new_edge_x1[0] = edge_x1
                        if new_edge_x2[0] == edge_x2:
                            new_edge_x2[1] += 1
                            if new_edge_x2[1] >= 20:
                                edge_x2= 0
                                new_edge_x2[1] = 0
                        else:
                            new_edge_x2[0] = edge_x2

                    except:
                        edge_x1, edge_x2 = image_draw_corner_of_computer(img[(y1):(y1 + down_line), x1:x2], edge_x1, edge_x2)
                    center[0].append(int((x1+x2)/2))
                    center[1].append(int((y1+y2)/2))
                    cv2.circle(img, center=(int((x1+x2)/2), int((y1+y2)/2)), radius=3, color=(0, 255, 0), thickness=4)



                    # confidence
                    confidence = math.ceil((box.conf[0] * 100)) / 100

                    print("Confidence --->", confidence)
                    # class name
                    # object details
                    org = [x1, y1]
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    fontScale = 1
                    color = (255, 0, 0)
                    thickness = 2
                if cls == 63:
                    break

        cv2.imshow('Webcam', img)
        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


detect_compuet_and_his_angle()