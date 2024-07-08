import cv2
import torch
import numpy as np
from ultralytics import YOLO
mport serial
import t
points = []
x='1'
def move_to_right():
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    ser.setDTR(False)
    time.sleep(1)
    ser.flushInput()
    ser.setDTR(True)
    time.sleep(2)
    ser.write(b'2')
    time.sleep(2)

def move_to_left():
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    ser.setDTR(False)
    time.sleep(1)
    ser.flushInput()
    ser.setDTR(True)
    time.sleep(2)
    ser.write(b'1')
    time.sleep(2)
def move_to_center():
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    ser.setDTR(False)
    time.sleep(1)
    ser.flushInput()
    ser.setDTR(True)
    time.sleep(2)
    ser.write(b'0')
    time.sleep(2)



def POINTS(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSEMOVE:
        colorsBGR = [x, y]
        print(colorsBGR)

def exist_trffic(smar,saml):
    trn_r=0
    trn_l=0
    if smar/2>saml:
        trn_r=1
        print("mm")
    elif saml/2>smar:
        trn_l=1
    saml = 0
    samr = 0
    return saml,samr,trn_l,trn_r


def main():
    cv2.namedWindow('FRAME')
    #cv2.setMouseCallback('FRAME', POINTS)

    model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
    #model = YOLO("yolov8l.pt")

    cap = cv2.VideoCapture('test1.mp4')
    count = 0
    area_right = [(670, 333), (780, 690), (1277, 589), (820, 315)]
    area_left = [(435, 316), (2, 600), (570, 665), (620, 330)]

    skip_fram = 1
    fram_count = 0
    saml = 0
    samr = 0
    Prev_count_left = 0
    Prev_count_right = 0
    kk = 0
    tl = 0
    tr = 0

    while True:
        tl=0
        tr=0
        kk = kk + 1

        ret, frame = cap.read()
        fram_count = +1

        if not ret:
            break
        if fram_count % skip_fram != 0:
            continue
        # frame = cv2.resize(frame, (1020, 600))
        frame = cv2.resize(frame, (1280, 720))
        results = model(frame)
        list_le = []
        list_re = []

        for index, row in results.pandas().xyxy[0].iterrows():
            x1 = int(row['xmin'])
            y1 = int(row['ymin'])
            x2 = int(row['xmax'])
            y2 = int(row['ymax'])
            d = (row['name'])
            cx = int(x1 + x2) // 2
            cy = int(y1 + y2) // 2

            if 'car' or 'bus' or 'trucks' in d:
                results = cv2.pointPolygonTest(np.array(area_left, np.int32), ((cx, cy)), False)
                if results >= 0:
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 3)
                    cv2.putText(frame, str(d), (x1, y1), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
                    list_le.append([cx])

            if 'car' or 'bus' or 'trucks' in d:
                results = cv2.pointPolygonTest(np.array(area_right, np.int32), ((cx, cy)), False)
                if results >= 0:
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 3)
                    cv2.putText(frame, str(d), (x1, y1), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
                    list_re.append([cx])

        cv2.polylines(frame, [np.array(area_right, np.int32)], True, (0, 255, 0), 2)
        count_right = len(list_re)
        cv2.putText(frame, str(count_right), (1200, 30), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
        ##############3
        cv2.polylines(frame, [np.array(area_left, np.int32)], True, (0, 255, 0), 2)
        count_left = len(list_le)
        cv2.putText(frame, str(count_left), (60, 30), cv2.FONT_HERSHEY_PLAIN, 2, (0,255, 0), 2)

        if count_left > 9:
            if Prev_count_left != count_left:
                saml = saml + 1
                Prev_count_left = count_left
        if count_right > 8:
            if Prev_count_right != count_right:
                samr = samr + 1
        if samr or saml > 20:
            saml, samr, tl, tr = exist_trffic(samr, saml)

        if tl==1:
            move_to_right()
        elif tr==1:
            move_to_left()
        elif count_right == count_left:
            move_to_center()
        cv2.putText(frame, str(saml), (60, 60), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255,0), 2)
        cv2.putText(frame, str(samr), (1200, 60), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
        cv2.putText(frame, str(tl), (1200, 90), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
        cv2.putText(frame, str(tr), (60, 90), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)







        cv2.imshow("FRAME", frame)
        #cv2.setMouseCallback("FRAME", POINTS)
        # to make vide run
        if cv2.waitKey(1) & 0xFF == 27:
            break
    cap.release()
    cv2.destroyAllWindows()
main()