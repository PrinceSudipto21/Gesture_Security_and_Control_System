#importing required libraries

from math import sqrt
from tkinter import SOLID
import math
import cv2
import mediapipe as mp
import numpy as np
import os, sys
import mysql.connector as msql


#Extracting hand recognition solution

mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=1)


#Assigning a variable to video capturing

cap = cv2.VideoCapture(0)


#extract unique serial number of system

os_t = sys.platform.lower()
if "win" in os_t:
    command = "wmic bios get serialnumber"
elif "linux" in os_t:
    command = "hal-get-property --udi /org/freedesktop/Hal/devices/computer --key system.hardware.uuid"
elif "darwin" in os_t:
    command = "ioreg -l | grep IOPlatformSerialNumber"
sn = os.popen(command).read().replace("\n","").replace("	","").replace(" ","").replace("SerialNumber",'')
sn = sn.lower()


#stablishing connection with database

conn = msql.connect(
  host="localhost",
  user="root",
  password="123456789"
)


#checking whether the required database is in the server

mycursor = conn.cursor()
if conn.is_connected():
    mycursor.execute("SHOW DATABASES")
    for x in mycursor:
        if sn in x:
            flag = 1
            break
        else:
            flag = 0
    print(flag)
else:
    print("Connection not stablished")
    cap.release()
    cv2.destroyAllWindows()


#Measurement prediction

X = [26, 27, 29, 31, 33, 35, 37, 39, 41, 43, 45, 47, 49, 51, 53, 55, 57, 59, 61, 63]    #measured length
Y = [161, 150, 139, 128, 118, 110, 104, 100, 94, 90, 84, 81, 79, 75, 73, 70, 66, 64, 62, 62]    #shown length between index 5 and 17
Z = [423, 392, 365, 348, 332, 310, 291, 274, 255, 243, 230, 224, 211, 205, 195, 188, 178, 170, 163, 161]    #shown length between index 0 and 12


#Cofficient calculation

coff = np.polyfit(Y, X, 2)
coff2 = np.polyfit(Z, Y, 2)

A, B, C = coff
D, E, F = coff2

A = (A+D)/2
B = (B+E)/2
C = (C+F)/2


while True:
    success, img = cap.read()   #img capture
    img = cv2.flip(img, 90)     #flipping the image
    
    if not success:            #condition if the image is not capturing
        break
    
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)      #converting image format from BGR to RGB
    results = hands.process(imgRGB)

    h, w, c = img.shape         #extracting image size
    
    if results.multi_hand_landmarks:        #condition if the palm detected
        x_arr = []        #it store x coordinates of 21 index points
        y_arr = []        #it store y coordinates of 21 index points
        dis_arr = []          #it store distance between required 21 index points

        for handLms in results.multi_hand_landmarks:        #accessing the coordinated of landmarks


            #marking the index points on palm

            for id, lm in enumerate(handLms.landmark):
                cx, cy = int(lm.x*w), int(lm.y*h)
                cv2.circle(img, (int(cx), int(cy)), 3, (10,10,10), cv2.FILLED)
                x_arr = x_arr[:id]+[cx]+x_arr[id+1:]
                y_arr = y_arr[:id]+[cy]+y_arr[id+1:]


            #joining the required index points and finding the distance between two index points

            for id, lm in enumerate(handLms.landmark):
                if id == 0:
                    cv2.line(img,(x_arr[0],y_arr[0]),(x_arr[1],y_arr[1]),(0,255,0),(2))
                    dis = math.trunc(sqrt(pow((x_arr[0] - x_arr[1]),2) + pow((y_arr[0] - y_arr[1]),2)))
                    dis = A * dis**2 + B*dis + C
                    dis_arr = dis_arr[:0]+[dis]+x_arr[0+1:]
                    cv2.line(img,(x_arr[0],y_arr[0]),(x_arr[5],y_arr[5]),(0,255,0),(2))
                    dis = math.trunc(sqrt(pow((x_arr[0] - x_arr[5]),2) + pow((y_arr[0] - y_arr[5]),2)))
                    dis = A * dis**2 + B*dis + C
                    dis_arr = dis_arr[:4]+[dis]+x_arr[4+1:]
                    cv2.line(img,(x_arr[0],y_arr[0]),(x_arr[17],y_arr[17]),(0,255,0),(2))
                    dis = math.trunc(sqrt(pow((x_arr[0] - x_arr[17]),2) + pow((y_arr[0] - y_arr[17]),2)))
                    dis = A * dis**2 + B*dis + C
                    dis_arr = dis_arr[:20]+[dis]+x_arr[20+1:]

                elif id == 1:
                    cv2.line(img,(x_arr[1],y_arr[1]),(x_arr[2],y_arr[2]),(0,255,0),(2))
                    dis = math.trunc(sqrt(pow((x_arr[1] - x_arr[2]),2) + pow((y_arr[1] - y_arr[2]),2)))
                    dis = A * dis**2 + B*dis + C
                    dis_arr = dis_arr[:1]+[dis]+x_arr[1+1:]

                elif id == 2:
                    cv2.line(img,(x_arr[2],y_arr[2]),(x_arr[3],y_arr[3]),(0,255,0),(2))
                    dis = math.trunc(sqrt(pow((x_arr[2] - x_arr[3]),2) + pow((y_arr[2] - y_arr[3]),2)))
                    dis = A * dis**2 + B*dis + C
                    dis_arr = dis_arr[:2]+[dis]+x_arr[2+1:]

                elif id == 3:
                    cv2.line(img,(x_arr[3],y_arr[3]),(x_arr[4],y_arr[4]),(0,255,0),(2))
                    dis = math.trunc(sqrt(pow((x_arr[3] - x_arr[4]),2) + pow((y_arr[3] - y_arr[4]),2)))
                    dis = A * dis**2 + B*dis + C
                    dis_arr = dis_arr[:3]+[dis]+x_arr[3+1:]

                elif id == 5:
                    cv2.line(img,(x_arr[5],y_arr[5]),(x_arr[9],y_arr[9]),(0,255,0),(2))
                    dis = math.trunc(sqrt(pow((x_arr[5] - x_arr[9]),2) + pow((y_arr[5] - y_arr[9]),2)))
                    dis = A * dis**2 + B*dis + C
                    dis_arr = dis_arr[:8]+[dis]+x_arr[8+1:]
                    cv2.line(img,(x_arr[5],y_arr[5]),(x_arr[6],y_arr[6]),(0,255,0),(2))
                    dis = math.trunc(sqrt(pow((x_arr[6] - x_arr[5]),2) + pow((y_arr[6] - y_arr[5]),2)))
                    dis = A * dis**2 + B*dis + C
                    dis_arr = dis_arr[:5]+[dis]+x_arr[5+1:]

                elif id == 6:
                    cv2.line(img,(x_arr[6],y_arr[6]),(x_arr[7],y_arr[7]),(0,255,0),(2))
                    dis = math.trunc(sqrt(pow((x_arr[6] - x_arr[7]),2) + pow((y_arr[6] - y_arr[7]),2)))
                    dis = A * dis**2 + B*dis + C
                    dis_arr = dis_arr[:6]+[dis]+x_arr[6+1:]

                elif id == 7:
                    cv2.line(img,(x_arr[7],y_arr[7]),(x_arr[8],y_arr[8]),(0,255,0),(2))
                    dis = math.trunc(sqrt(pow((x_arr[8] - x_arr[7]),2) + pow((y_arr[8] - y_arr[7]),2)))
                    dis = A * dis**2 + B*dis + C
                    dis_arr = dis_arr[:7]+[dis]+x_arr[7+1:]

                elif id == 9:
                    cv2.line(img,(x_arr[9],y_arr[9]),(x_arr[13],y_arr[13]),(0,255,0),(2))
                    dis = math.trunc(sqrt(pow((x_arr[9] - x_arr[13]),2) + pow((y_arr[9] - y_arr[13]),2)))
                    dis = A * dis**2 + B*dis + C
                    dis_arr = dis_arr[:12]+[dis]+x_arr[12+1:]
                    cv2.line(img,(x_arr[9],y_arr[9]),(x_arr[10],y_arr[10]),(0,255,0),(2))
                    dis = math.trunc(sqrt(pow((x_arr[9] - x_arr[10]),2) + pow((y_arr[9] - y_arr[10]),2)))
                    dis = A * dis**2 + B*dis + C
                    dis_arr = dis_arr[:9]+[dis]+x_arr[9+1:]

                elif id == 10:
                    cv2.line(img,(x_arr[10],y_arr[10]),(x_arr[11],y_arr[11]),(0,255,0),(2))
                    dis = math.trunc(sqrt(pow((x_arr[10] - x_arr[11]),2) + pow((y_arr[10] - y_arr[11]),2)))
                    dis = A * dis**2 + B*dis + C
                    dis_arr = dis_arr[:10]+[dis]+x_arr[10+1:]

                elif id == 11:
                    cv2.line(img,(x_arr[11],y_arr[11]),(x_arr[12],y_arr[12]),(0,255,0),(2))
                    dis = math.trunc(sqrt(pow((x_arr[11] - x_arr[12]),2) + pow((y_arr[11] - y_arr[12]),2)))
                    dis = A * dis**2 + B*dis + C
                    dis_arr = dis_arr[:11]+[dis]+x_arr[11+1:]

                elif id == 13:
                    cv2.line(img,(x_arr[17],y_arr[17]),(x_arr[13],y_arr[13]),(0,255,0),(2))
                    dis = math.trunc(sqrt(pow((x_arr[13] - x_arr[17]),2) + pow((y_arr[13] - y_arr[17]),2)))
                    dis = A * dis**2 + B*dis + C
                    dis_arr = dis_arr[:16]+[dis]+x_arr[16+1:]
                    cv2.line(img,(x_arr[13],y_arr[13]),(x_arr[14],y_arr[14]),(0,255,0),(2))
                    dis = math.trunc(sqrt(pow((x_arr[13] - x_arr[14]),2) + pow((y_arr[13] - y_arr[14]),2)))
                    dis = A * dis**2 + B*dis + C
                    dis_arr = dis_arr[:13]+[dis]+x_arr[13+1:]

                elif id == 14:
                    cv2.line(img,(x_arr[14],y_arr[14]),(x_arr[15],y_arr[15]),(0,255,0),(2))
                    dis = math.trunc(sqrt(pow((x_arr[14] - x_arr[15]),2) + pow((y_arr[14] - y_arr[15]),2)))
                    dis = A * dis**2 + B*dis + C
                    dis_arr = dis_arr[:14]+[dis]+x_arr[14+1:]

                elif id == 15:
                    cv2.line(img,(x_arr[15],y_arr[15]),(x_arr[16],y_arr[16]),(0,255,0),(2))
                    dis = math.trunc(sqrt(pow((x_arr[16] - x_arr[15]),2) + pow((y_arr[16] - y_arr[15]),2)))
                    dis = A * dis**2 + B*dis + C
                    dis_arr = dis_arr[:15]+[dis]+x_arr[15+1:]

                elif id == 17:
                    cv2.line(img,(x_arr[17],y_arr[17]),(x_arr[18],y_arr[18]),(0,255,0),(2))
                    dis = math.trunc(sqrt(pow((x_arr[17] - x_arr[18]),2) + pow((y_arr[17] - y_arr[18]),2)))
                    dis = A * dis**2 + B*dis + C
                    dis_arr = dis_arr[:17]+[dis]+x_arr[17+1:]

                elif id == 18:
                    cv2.line(img,(x_arr[18],y_arr[18]),(x_arr[19],y_arr[19]),(0,255,0),(2))
                    dis = math.trunc(sqrt(pow((x_arr[18] - x_arr[19]),2) + pow((y_arr[18] - y_arr[19]),2)))
                    dis = A * dis**2 + B*dis + C
                    dis_arr = dis_arr[:18]+[dis]+x_arr[18+1:]

                elif id == 19:
                    cv2.line(img,(x_arr[19],y_arr[19]),(x_arr[20],y_arr[20]),(0,255,0),(2))
                    dis = math.trunc(sqrt(pow((x_arr[19] - x_arr[20]),2) + pow((y_arr[19] - y_arr[20]),2)))
                    dis = A * dis**2 + B*dis + C
                    dis_arr = dis_arr[:19]+[dis]+x_arr[19+1:]


        #data fenching and matching from database

        #if required database not exist in the server
        if flag == 0:
            mycursor.execute("CREATE DATABASE %s" %sn)
            cv2.putText(img, 'This system is new.', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
        
        #if required database exist in the server
        else:
            cv2.putText(img, 'HI.', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)

    cv2.imshow("Gesture Security and Control System", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()