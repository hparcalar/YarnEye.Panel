import numpy as np
import cv2 as cv2
import socket
import requests
import time
import json
from requests.exceptions import ConnectionError

hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)
print('<<< HEKA YARN TESTER IS RUNNING ON: ' + local_ip + ' >>>')

# WindowName="HEKA YARN TESTER"
# view_window = cv2.namedWindow(WindowName,cv2.WINDOW_NORMAL)
#
# # These two lines will force the window to be on top with focus.
# cv2.setWindowProperty(WindowName,cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
# cv2.setWindowProperty(WindowName,cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_NORMAL)

testerData = None
targetHue = 0.0
targetSat = 0.0
targetVal = 0.0

def circleRadius(p):
    return p[0, 2]


def yarnCapture():
    cap = cv2.VideoCapture(0)
    # cap.set(cv2.CAP_PROP_EXPOSURE, 0)
    kernel = np.ones((5, 5), np.uint8)
    hue=0.0
    sat=0.0
    val=0.0

    while True:
        ret, frame = cap.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        output = frame.copy()

        # BOBİNİ BUL
        roi = None
        circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1.2, 100, param1=120,
                  param2=80,
                  minRadius=290,
                  maxRadius=360)
        try:
            if circles is not None:
                # BOBİN DAİRE ÇEVRESİNİ ÇİZDİR
                biggestCircle = max(circles, key=circleRadius)
                biggestCircle = biggestCircle[0, :]
                cv2.circle(output, (int(biggestCircle[0]), int(biggestCircle[1])), int(biggestCircle[2]), (0, 255, 0), 2)
                cv2.circle(output, (int(biggestCircle[0]), int(biggestCircle[1])), 2, (0, 0, 255), 3)
                x, y, r = biggestCircle.astype(np.int32)
                roi = hsv[y - r: y + r, x - r: x + r]
        except ValueError as err:
            print("Circle is not found" + str(err))

        # BOBİN MASKESİNİ OLUŞTUR
        if roi is not None:
            try:
                width, height = roi.shape[:2]
                mask = np.zeros((width, height, 3), roi.dtype)
                cv2.circle(mask, (int(width / 2), int(height / 2)), r, (255, 255, 255), -1)

                dst = cv2.bitwise_and(roi, mask)

                # filter black color and fetch color values
                data = []
                for i in range(3):
                    try:
                        channel = dst[:, :, i]
                        indices = np.where(channel != 0)[0]
                        color = np.mean(channel[indices])
                        data.append(color)
                    except ValueError as err:
                        print("err")
                    except TypeError as err:
                        print("err")

                # opencv images are in bgr format
                hue, sat, val = data

                # print(data)

                # OLMASI GEREKEN İPLİK RENK TONLARI
                truthPath = np.array([targetHue, targetSat, targetVal])

                # FARK DEĞERLERİ
                diffPath = truthPath - np.array(data)

                # cv2.putText(output, 'H: ' + str(hue), (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)
                # cv2.putText(output, 'S: ' + str(sat), (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)
                # cv2.putText(output, 'V: ' + str(val), (20, 110), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)

                if abs(diffPath[0]) >= 15 or abs(diffPath[1]) >= 15:
                    cv2.putText(output, 'TON FARKI VAR', (20,70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 4)
                else:
                    cv2.putText(output, 'OK', (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 4)
            except ValueError as errV:
                print(errV)

        cv2.putText(output, 'Q: TESTI KAPAT', (20,150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 4)
        cv2.imshow('HEKA YARN TESTER', cv2.resize(output, (1600, 800)))
        if cv2.waitKey(1) == ord('q'):
            postData = {'activeTesterId': 0,
                        'ipAddr': str(local_ip),
                        'prodLineId': testerData['prodLineId'],
                        'testerStatus': 2}
            headerObj = {
                             'Content-Type': 'application/json',
                             'Accept': 'text/plain'
                        }
            requests.post("http://localhost:5000/ActiveTester", data=json.dumps(postData),
                                         headers=headerObj).json()
            break

    cap.release()
    cv2.destroyAllWindows()


while True:
    try:
        response = requests.get("http://localhost:5000/ActiveTester?hostname=" + str(local_ip))
        testerData = response.json()
        if testerData['prodLineId'] is not None and testerData['testerStatus'] == 1:
            responseColors = requests.get("http://localhost:5000/ColorAssignment/ProdLine/" + str(testerData['prodLineId'])).json()
            if responseColors['assignmentId'] > 0:
                targetHue = responseColors['setHue']
                targetSat = responseColors['setSaturation']
                targetVal = responseColors['setValue']
                yarnCapture()
    except ConnectionError as errConn:
        print(errConn)
    except TypeError as errT:
        print(errT)
    time.sleep(2)
