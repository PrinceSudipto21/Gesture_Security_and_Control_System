from tkinter import SOLID
import cv2
import mediapipe as mp

mpHands = mp.solutions.hands
hands = mpHands.Hands() 

cap = cv2.VideoCapture(0) 
x_arr = [21]
y_arr = [21]
while True:
    success, img = cap.read()
    
    if not success: 
        break
    
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    h, w, c = img.shape
    
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                cx, cy = int(lm.x*w), int(lm.y*h)
                cv2.circle(img, (int(cx), int(cy)), 3, (10,10,10), cv2.FILLED)
                x_arr = x_arr[:id]+[cx]+x_arr[id+1:]
                y_arr = y_arr[:id]+[cy]+y_arr[id+1:]
            for id, lm in enumerate(handLms.landmark):
                if id == 0:
                    cv2.line(img,(x_arr[0],y_arr[0]),(x_arr[1],y_arr[1]),(0,255,0),(2))
                    cv2.line(img,(x_arr[0],y_arr[0]),(x_arr[5],y_arr[5]),(0,255,0),(2))
                    cv2.line(img,(x_arr[0],y_arr[0]),(x_arr[17],y_arr[17]),(0,255,0),(2))
                elif id == 1:
                    cv2.line(img,(x_arr[1],y_arr[1]),(x_arr[2],y_arr[2]),(0,255,0),(2))
                elif id == 2:
                    cv2.line(img,(x_arr[2],y_arr[2]),(x_arr[3],y_arr[3]),(0,255,0),(2))
                elif id == 3:
                    cv2.line(img,(x_arr[3],y_arr[3]),(x_arr[4],y_arr[4]),(0,255,0),(2))
                elif id == 5:
                    cv2.line(img,(x_arr[5],y_arr[5]),(x_arr[9],y_arr[9]),(0,255,0),(2))
                    cv2.line(img,(x_arr[5],y_arr[5]),(x_arr[6],y_arr[6]),(0,255,0),(2))
                elif id == 6:
                    cv2.line(img,(x_arr[6],y_arr[6]),(x_arr[7],y_arr[7]),(0,255,0),(2))
                elif id == 7:
                    cv2.line(img,(x_arr[7],y_arr[7]),(x_arr[8],y_arr[8]),(0,255,0),(2))
                elif id == 9:
                    cv2.line(img,(x_arr[9],y_arr[9]),(x_arr[13],y_arr[13]),(0,255,0),(2))
                    cv2.line(img,(x_arr[9],y_arr[9]),(x_arr[10],y_arr[10]),(0,255,0),(2))
                elif id == 10:
                    cv2.line(img,(x_arr[10],y_arr[10]),(x_arr[11],y_arr[11]),(0,255,0),(2))
                elif id == 11:
                    cv2.line(img,(x_arr[11],y_arr[11]),(x_arr[12],y_arr[12]),(0,255,0),(2))
                elif id == 13:
                    cv2.line(img,(x_arr[17],y_arr[17]),(x_arr[13],y_arr[13]),(0,255,0),(2))
                    cv2.line(img,(x_arr[13],y_arr[13]),(x_arr[14],y_arr[14]),(0,255,0),(2))
                elif id == 14:
                    cv2.line(img,(x_arr[14],y_arr[14]),(x_arr[15],y_arr[15]),(0,255,0),(2))
                elif id == 15:
                    cv2.line(img,(x_arr[15],y_arr[15]),(x_arr[16],y_arr[16]),(0,255,0),(2))
                elif id == 17:
                    cv2.line(img,(x_arr[17],y_arr[17]),(x_arr[18],y_arr[18]),(0,255,0),(2))
                elif id == 18:
                    cv2.line(img,(x_arr[18],y_arr[18]),(x_arr[19],y_arr[19]),(0,255,0),(2))
                elif id == 19:
                    cv2.line(img,(x_arr[19],y_arr[19]),(x_arr[20],y_arr[20]),(0,255,0),(2))
    cv2.imshow("Image", img)
    
    if cv2.waitKey(1) == ord('q'):
        break  
        
cap.release()
cv2.destroyAllWindows()