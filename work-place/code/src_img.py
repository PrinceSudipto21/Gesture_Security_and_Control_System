<<<<<<< HEAD
from tkinter import SOLID
=======
>>>>>>> ee5c0b98a1ada5c40994328fd9e34ee3bd30c40c
import cv2
import mediapipe as mp
cap = cv2.VideoCapture(0) # Replace with your own video and webcam

mpHands = mp.solutions.hands
hands = mpHands.Hands() 

def coordinate(id, h, w):
    cx, cy = lm.x*w, lm.y*h
<<<<<<< HEAD
    cv2.circle(img, (int(cx), int(cy)), 3, (255,255,255), cv2.FILLED)
=======
    cv2.circle(img, (int(cx), int(cy)), 1, (255,255,255), cv2.FILLED)  
>>>>>>> ee5c0b98a1ada5c40994328fd9e34ee3bd30c40c
    return cx, cy

while True:
    success, img = cap.read()
    
    if not success: 
        break
    
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    h, w, c = img.shape
    handsup=0
    thumbs_correct=0
    fingers_correct=0
    
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                if id == 0: 
                    __, cy_0 = coordinate(0, h, w)
                if id == 10: 
                    __, cy_10 = coordinate(10, h, w)
                if id == 1: 
                    __, cy_1 = coordinate(1, h, w)
                if id == 2:
                    __, cy_2 = coordinate(2, h, w)
                if id == 3:
                    __, cy_3 = coordinate(3, h, w)
                if id == 4: 
                    __, cy_4 = coordinate(4, h, w)
                if id == 5: 
                    __, cy_5 = coordinate(5, h, w)
                if id == 9: 
                    __, cy_9 = coordinate(9, h, w)
                if id == 13: 
                    __, cy_13 = coordinate(13, h, w)
                if id == 17: 
                    __, cy_17 = coordinate(17, h, w)
                if id == 6: 
                    __, cy_6 = coordinate(6, h, w)    
                if id == 8: 
                    __, cy_8 = coordinate(8, h, w)  
                if id == 12: 
                    __, cy_12 = coordinate(12, h, w)
                if id == 16: 
                    __, cy_16 = coordinate(16, h, w)
                if id == 20: 
                    __, cy_20 = coordinate(20, h, w)
                if id == 7: 
                    __, cy_7 = coordinate(7, h, w)
                if id == 11: 
                    __, cy_11 = coordinate(11, h, w)
                if id == 14: 
                    __, cy_14 = coordinate(14, h, w)
                if id == 15: 
                    __, cy_15 = coordinate(15, h, w)
                if id == 18: 
                    __, cy_18 = coordinate(18, h, w)
                if id == 19: 
                    __, cy_19 = coordinate(19, h, w)
                if id == 20: 
                    __, cy_20 = coordinate(20, h, w)

            if cy_10 < cy_0:
                handsup=1
            else:
                handsup=0
                    
            if (cy_2 > cy_10 and cy_2 < cy_0) and (cy_3 > cy_10 and cy_3 < cy_0):
                thumbs_correct=1
            else:
                thumbs_correct=0
            
            if (cy_5 < cy_8) and (cy_9 < cy_12) and (cy_13 < cy_16) and (cy_17 < cy_20):
                fingers_correct=1
            else:
                figners_correct=0
            
<<<<<<< HEAD
=======
            if handsup==1 and thumbs_correct==1 and fingers_correct==1 and Take_photo==0:
                Take_photo=120

>>>>>>> ee5c0b98a1ada5c40994328fd9e34ee3bd30c40c
    cv2.imshow("Image", img)
    
    if cv2.waitKey(10) & 0xFF==ord('q'):
        break  
        
cap.release()
cv2.destroyAllWindows()

cv2.waitKey(0)
cv2.destroyAllWindows()
