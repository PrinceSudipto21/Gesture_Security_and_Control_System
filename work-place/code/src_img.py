
mpHands = mp.solutions.hands
hands = mpHands.Hands() 

cap = cv2.VideoCapture(0) # Replace with your own video and webcam

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
            
    cv2.imshow("Image", img)
    
    if cv2.waitKey(10) & 0xFF==ord('q'):
        break  
        
cap.release()
cv2.destroyAllWindows()