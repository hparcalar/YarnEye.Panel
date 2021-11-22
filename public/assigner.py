import numpy as np
import cv2 as cv2
import socket
import requests
import time
import json
from requests.exceptions import ConnectionError

hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)
print('<<< HEKA YARN ASSIGNER IS RUNNING ON: ' + local_ip + ' >>>')

# WindowName="HEKA YARN ASSIGNER"
# view_window = cv2.namedWindow(WindowName,cv2.WINDOW_NORMAL)
#
# # These two lines will force the window to be on top with focus.
# cv2.setWindowProperty(WindowName,cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
# cv2.setWindowProperty(WindowName,cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_NORMAL)

assignerData = None


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

                # opencv images are in bgr format
                hue, sat, val = data

                # print(data)

                # OLMASI GEREKEN İPLİK RENK TONLARI
                #truthPath = np.array([106.23460494599563, 40.723084323384526, 161.74960387867813])
                truthPath = np.array([118.61295396121527, 13.219286308225259, 163.66545426010126])

                # FARK DEĞERLERİ
                diffPath = truthPath - np.array(data)

                cv2.putText(output, 'H: ' + str(hue), (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)
                cv2.putText(output, 'S: ' + str(sat), (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)
                cv2.putText(output, 'V: ' + str(val), (20, 110), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)

                # if abs(diffPath[0]) >= 11 or abs(diffPath[1]) >= 11:
                #     cv2.putText(output, 'TON FARKI VAR', (20,70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 4)
                # else:
                #     cv2.putText(output, 'OK', (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 4)
            except ValueError as errV:
                print(errV)

        cv2.putText(output, 'Q: SECIMI TAMAMLA', (20,150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 4)
        cv2.imshow('HEKA YARN ASSIGNER', cv2.resize(output, (1600, 800)))
        if cv2.waitKey(1) == ord('q'):
            postData = {'activeAssignerId': 0,
                        'ipAddr': str(local_ip),
                        'selectedLines': assignerData['selectedLines'],
                        'assignerStatus': 2}
            headerObj = {
                             'Content-Type': 'application/json',
                             'Accept': 'text/plain'
                        }
            responsePost = requests.post("http://localhost:5000/ActiveAssigner", data=json.dumps(postData),
                                         headers=headerObj).json()
            if responsePost['result']:
                responsePost = requests.post("http://localhost:5000/ColorAssignment",
                                             headers=headerObj,
                                             data=json.dumps({'assignmentId':0,
                                                            'assignmentCode':'',
                                                            'isActive': True,
                                                            'setHue':hue,
                                                            'setSaturation': sat,
                                                            'setValue': val})).json()
                if responsePost['result'] and responsePost['recordId'] > 0:
                    assignmentLines = assignerData['selectedLines'].split(',')
                    for line in assignmentLines:
                        requests.post("http://localhost:5000/ProdLine",
                                                     headers=headerObj,
                                                     data=json.dumps({'prodLineId': int(line),
                                                                      'prodLineCode': '',
                                                                      'prodLineName': '',
                                                                      'assignmentId': int(responsePost['recordId'])}))
            break

    cap.release()
    cv2.destroyAllWindows()


while True:
    try:
        response = requests.get("http://localhost:5000/ActiveAssigner?hostname=" + str(local_ip))
        assignerData = response.json()
        if assignerData['selectedLines'] is not None and assignerData['assignerStatus'] == 1:
            yarnCapture()
    except ConnectionError as errConn:
        print(errConn)
    time.sleep(2)
