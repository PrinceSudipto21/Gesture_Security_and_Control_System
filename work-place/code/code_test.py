from math import sqrt
from tkinter import SOLID
import math
import cv2
import mediapipe as mp
import numpy as np
import os
import sys
import mysql.connector as msql
import time

def security():
    # if required database not exist in the server
    global mycursor, flag, a, initial, securityEnter
    securityEnter = 1
    if flag == 0:
        mycursor.execute('CREATE TABLE Admins(PersonID int not null auto_increment, index_0 float, index_1 float, index_2 float, index_3 float, index_4 float, index_5 float, index_6 float, index_7 float, index_8 float, index_9 float, index_10 float, index_11 float, index_12 float, index_13 float, index_14 float, index_15 float, index_16 float, index_17 float, index_18 float, index_19 float, index_20 float, primary key (PersonID))')
        addAdmins()
        flag = 2
    # if required database is already exist in the server
    elif flag == 1:
        mycursor.execute('select index_0, index_1, index_2, index_3, index_4, index_5, index_6, index_7, index_8, index_9, index_10, index_11, index_12, index_13, index_14, index_15, index_16, index_17, index_18, index_19, index_20 from Admins')
        for j in mycursor:
            for i in range(21):
                if error(dis_arr[i], j[i]) >= 90:
                    a=a+1
                else:
                    break
        initial = time.time()

def error(dis, i):
    if dis > i:
        b = (i/dis)*100
    elif i > dis:
        b = (dis/i)*100
    else:
        b = 100
    return b

def addAdmins():
    global mycursor, conn, dis_arr, initial
    mycursor.execute('insert into Admins (index_0, index_1, index_2, index_3, index_4, index_5, index_6, index_7, index_8, index_9, index_10, index_11, index_12, index_13, index_14, index_15, index_16, index_17, index_18, index_19, index_20) values(%f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f)' % (
        dis_arr[0], dis_arr[1], dis_arr[2], dis_arr[3], dis_arr[4], dis_arr[5], dis_arr[6], dis_arr[7], dis_arr[8], dis_arr[9], dis_arr[10], dis_arr[11], dis_arr[12], dis_arr[13], dis_arr[14], dis_arr[15], dis_arr[16], dis_arr[17], dis_arr[18], dis_arr[19], dis_arr[20]))
    conn.commit()

def wait1():
    global initial, k, temp, count, img
    if k == 0:
        cv2.putText(img, 'This system is already exist. So, lets check your palm.',
                    (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2, cv2.LINE_AA)
        if time.time() - initial >= 5:
            k = 1
            initial = time.time()
        temp = 0
    elif k == 1:
        cv2.putText(img, 'Place your palm in the correct position in front of camera within 10 sec.',
                    (5, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.53, (255, 0, 0), 1, cv2.LINE_AA)
        cv2.putText(img, 'Otherwise system will not unlock.', (5, 70),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 1, cv2.LINE_AA)
        if time.time() - initial >= 5:
            k = 2
            initial = time.time() + 11
        temp = 0
    elif k == 2:
        cv2.putText(img, 'Try to properly fit your palm inside the square.',
                    (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2, cv2.LINE_AA)
        cv2.rectangle(img, (150, 80), (500, 430), (225, 0, 0), 2)
        cv2.putText(img, str(count), (260, 300),
                    cv2.FONT_HERSHEY_SIMPLEX, 5, (255, 0, 0), 2, cv2.LINE_AA)
        count = int(initial - time.time())
        if initial - time.time() < 1:
            temp = 1
    return temp

def wait():
    global initial, k, temp, count
    if k == 0:
        cv2.putText(img, 'This system is new. So, lets read your palm.',
                    (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2, cv2.LINE_AA)
        if time.time() - initial >= 5:
            k = 1
            initial = time.time()
        temp = 0
    elif k == 1:
        cv2.putText(img, 'Place your palm in the correct position in front of camera within 10 sec.',
                    (5, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.53, (255, 0, 0), 1, cv2.LINE_AA)
        cv2.putText(img, 'Otherwise it can cause security error.', (5, 70),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 1, cv2.LINE_AA)
        if time.time() - initial >= 5:
            k = 2
            initial = time.time() + 11
        temp = 0
    elif k == 2:
        cv2.putText(img, 'Try to properly fit your palm inside the square.',
                    (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2, cv2.LINE_AA)
        cv2.rectangle(img, (150, 80), (500, 430), (225, 0, 0), 2)
        cv2.putText(img, str(count), (260, 300),
                    cv2.FONT_HERSHEY_SIMPLEX, 5, (255, 0, 0), 2, cv2.LINE_AA)
        count = int(initial - time.time())
        if initial - time.time() < 1:
            return 1
    return temp

def connected():
    global conn, mycursor
    mycursor.execute("SHOW DATABASES")
    for x in mycursor:
        if sn in x:
            conn, mycursor = connecting(1)
            return 1
        else:
            continue
    mycursor.execute("CREATE DATABASE %s" % sn)
    connecting(1)
    return 0

def connecting(j):
    global conn, mycursor
    if j == 0:
        conn = msql.connect(host="localhost", user="root",
                            password="123456789")
        mycursor = conn.cursor()
    if j == 1:
        conn = msql.connect(host="localhost", user="root",
                            password="123456789", database=sn)
        mycursor = conn.cursor()
    return conn, mycursor

def serialNumber():
    os_t = sys.platform.lower()
    if "win" in os_t:
        command = "wmic bios get serialnumber"
    elif "linux" in os_t:
        command = "hal-get-property --udi /org/freedesktop/Hal/devices/computer --key system.hardware.uuid"
    elif "darwin" in os_t:
        command = "ioreg -l | grep IOPlatformSerialNumber"
    sn = os.popen(command).read().replace("\n", "").replace(
        "	", "").replace(" ", "").replace("SerialNumber", '')
    return sn.lower()

def coefficient():
    # Measurement prediction
    X = [26, 27, 29, 31, 33, 35, 37, 39, 41, 43, 45, 47,
         49, 51, 53, 55, 57, 59, 61, 63]  # measured length
    Y = [161, 150, 139, 128, 118, 110, 104, 100, 94, 90, 84, 81, 79, 75,
         73, 70, 66, 64, 62, 62]  # shown length between index 5 and 17
    Z = [423, 392, 365, 348, 332, 310, 291, 274, 255, 243, 230, 224, 211, 205,
         195, 188, 178, 170, 163, 161]  # shown length between index 0 and 12
    # Cofficient calculation
    coff = np.polyfit(Y, X, 2)
    coff2 = np.polyfit(Z, Y, 2)
    A, B, C = coff
    D, E, F = coff2
    A = (A+D)/2
    B = (B+E)/2
    C = (C+F)/2
    return A, B, C

def distanceAndPalmLine(x_arr, y_arr, dis_arr, n, m, A, B, C, i):
    cv2.line(img, (x_arr[n], y_arr[n]), (x_arr[m], y_arr[m]), (0, 255, 0), (2))
    dis = math.trunc(
        sqrt(pow((x_arr[n] - x_arr[m]), 2) + pow((y_arr[n] - y_arr[m]), 2)))
    dis = A * dis**2 + B*dis + C
    dis_arr = dis_arr[:i]+[float(dis)]+dis_arr[i+1:]
    return dis_arr

def mark_index(x_arr, y_arr, id, lm):
    cx, cy = int(lm.x*w), int(lm.y*h)
    cv2.circle(img, (int(cx), int(cy)), 3, (10, 10, 10), cv2.FILLED)
    x_arr = x_arr[:id]+[cx]+x_arr[id+1:]
    y_arr = y_arr[:id]+[cy]+y_arr[id+1:]
    return x_arr, y_arr

def join_index(x_arr, y_arr, dis_arr, id, A, B, C):
    if id == 0:
        dis_arr = distanceAndPalmLine(x_arr, y_arr, dis_arr, 0, 1, A, B, C, 0)
    elif id == 1:
        dis_arr = distanceAndPalmLine(x_arr, y_arr, dis_arr, 1, 2, A, B, C, 1)
    elif id == 2:
        dis_arr = distanceAndPalmLine(x_arr, y_arr, dis_arr, 2, 3, A, B, C, 2)
    elif id == 3:
        dis_arr = distanceAndPalmLine(x_arr, y_arr, dis_arr, 3, 4, A, B, C, 3)
    elif id == 4:
        dis_arr = distanceAndPalmLine(x_arr, y_arr, dis_arr, 0, 5, A, B, C, 4)
    elif id == 5:
        dis_arr = distanceAndPalmLine(x_arr, y_arr, dis_arr, 6, 5, A, B, C, 5)
    elif id == 6:
        dis_arr = distanceAndPalmLine(x_arr, y_arr, dis_arr, 6, 7, A, B, C, 6)
    elif id == 7:
        dis_arr = distanceAndPalmLine(x_arr, y_arr, dis_arr, 7, 8, A, B, C, 7)
    elif id == 8:
        dis_arr = distanceAndPalmLine(x_arr, y_arr, dis_arr, 5, 9, A, B, C, 8)
    elif id == 9:
        dis_arr = distanceAndPalmLine(x_arr, y_arr, dis_arr, 9, 10, A, B, C, 9)
    elif id == 10:
        dis_arr = distanceAndPalmLine(
            x_arr, y_arr, dis_arr, 10, 11, A, B, C, 10)
    elif id == 11:
        dis_arr = distanceAndPalmLine(
            x_arr, y_arr, dis_arr, 11, 12, A, B, C, 11)
    elif id == 12:
        dis_arr = distanceAndPalmLine(
            x_arr, y_arr, dis_arr, 9, 13, A, B, C, 12)
    elif id == 13:
        dis_arr = distanceAndPalmLine(
            x_arr, y_arr, dis_arr, 13, 14, A, B, C, 13)
    elif id == 14:
        dis_arr = distanceAndPalmLine(
            x_arr, y_arr, dis_arr, 14, 15, A, B, C, 14)
    elif id == 15:
        dis_arr = distanceAndPalmLine(
            x_arr, y_arr, dis_arr, 15, 16, A, B, C, 15)
    elif id == 16:
        dis_arr = distanceAndPalmLine(
            x_arr, y_arr, dis_arr, 17, 13, A, B, C, 16)
    elif id == 17:
        dis_arr = distanceAndPalmLine(
            x_arr, y_arr, dis_arr, 17, 18, A, B, C, 17)
    elif id == 18:
        dis_arr = distanceAndPalmLine(
            x_arr, y_arr, dis_arr, 18, 19, A, B, C, 18)
    elif id == 19:
        dis_arr = distanceAndPalmLine(
            x_arr, y_arr, dis_arr, 19, 20, A, B, C, 19)
    elif id == 20:
        dis_arr = distanceAndPalmLine(
            x_arr, y_arr, dis_arr, 0, 17, A, B, C, 20)
    return dis_arr

def palm_detected():
    x_arr = []      # it store x coordinates of 21 index points
    y_arr = []      # it store y coordinates of 21 index points
    dis_arr = []        # it store distance between required 21 index points
    for handLms in results.multi_hand_landmarks:  # accessing the coordinated of landmarks
        # marking the index points on palm
        for id, lm in enumerate(handLms.landmark):
            x_arr, y_arr = mark_index(x_arr, y_arr, id, lm)
        # joining the required index points and finding the distance between two index points
        for id, lm in enumerate(handLms.landmark):
            dis_arr = join_index(x_arr, y_arr, dis_arr, id, A, B, C)
    return dis_arr

#-------------------------------------------------------- CODE INITIATES -----------------------------------------------------------

# Extracting hand recognition solution
mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=1)

# Assigning a variable to video capturing
cap = cv2.VideoCapture(0)

# extract unique serial number of system
sn = serialNumber()

# coefficient
A, B, C = coefficient()

# stablishing connection with database
conn, mycursor = connecting(0)

# checking whether the required database is in the server
if conn.is_connected():
    flag = connected()
else:
    print("Connection can't be stablished")
    cap.release()
    cv2.destroyAllWindows()

temp = 0  # variable to confirm whether it has been entered into wait1() or wait()
initial = time.time()  # variable for time
k = 0
count = 10
a = 0
s = 0
securityEnter = 0

while True:
    success, img = cap.read()  # image capture
    img = cv2.flip(img, 90)  # flipping the image

    if not success:  # condition if the image is not capturing
        break

    # converting image format from BGR to RGB
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    h, w, c = img.shape  # extracting image size

    if temp == 0 and flag == 0:
        temp = wait()
    if temp == 0 and flag == 1:
        temp = wait1()

    if results.multi_hand_landmarks and temp == 1:

        dis_arr = palm_detected()

        # data fenching and matching from database
        if s == 0 or securityEnter == 1:
            if securityEnter == 0:
                security()
            if flag == 2 and (time.time()-initial <= 5):
                cv2.putText(img, 'ADMIN ADDED', (20, 300), cv2.FONT_HERSHEY_SIMPLEX, 5, (255, 0, 0), 2, cv2.LINE_AA)
            elif a == 21 and (time.time()-initial <= 5):
                cv2.putText(img, 'UNLOCK', (20, 300), cv2.FONT_HERSHEY_SIMPLEX, 5, (255, 0, 0), 2, cv2.LINE_AA)
            elif time.time()-initial <= 5:
                cv2.putText(img, 'LOCK', (20, 300), cv2.FONT_HERSHEY_SIMPLEX, 5, (0, 0, 255), 2, cv2.LINE_AA)
            else:
                securityEnter = 2

    cv2.imshow("Gesture Security and Control System", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
