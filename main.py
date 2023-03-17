import cv2
import cvzone
import numpy as np

from cvzone.HandTrackingModule import HandDetector

vid = cv2.VideoCapture(0)
vid.set(3, 1024)
vid.set(4, 576)


imgbkgrnd = cv2.imread("resources/pong_table_large_V2.png")
imgGameOver = cv2.imread("resources/game_over_V2.png")
pongBall = cv2.imread("resources/pong_Ball_small_V3.png",cv2.IMREAD_UNCHANGED)
pongBatleft = cv2.imread("resources/pong_bat.png",cv2.IMREAD_UNCHANGED)
pongBatright = cv2.imread("resources/pong_bat_right.png",cv2.IMREAD_UNCHANGED)
print(imgbkgrnd.shape)

#-------- Hand Detector ----------------
detector = HandDetector(detectionCon=0.8, maxHands=2)


# ------------ Ball movenent controls ---------------
ballPos = [150, 50]
speedX = 7
speedY = 7
score = [0,0]

while True:
    _, img = vid.read()
    img = cv2.flip(img, 1)
    #print(img.shape)
    
    #Find Hand and its landmarks
    hands, img = detector.findHands(img, flipType=False)
    
    
    
    #img = cvzone.overlayPNG(imgbkgrnd, img, [0,0])
    img = cv2.addWeighted(img,0.1,imgbkgrnd,0.9,0)
    
    #Check for hands
    if hands:
        for hand in hands:
            x, y, w, h = hand['bbox']
            h1, w1, _ = pongBatleft.shape
            y1 = y - int(h1/2)
            y1 = np.clip(y1, 20, 310)
            
            if hand["type"] == "Left":
                img = cvzone.overlayPNG(img, pongBatleft, [40, y1])
                if 35 < ballPos[0] < 35+w1 and y1 < ballPos[1] < y1 + h1:
                    speedX = -speedX
                    ballPos[0] += 30
                    score[0] += 1
                                    
            if hand["type"] == "Right":
                img = cvzone.overlayPNG(img, pongBatright, [905, y1])
                if 900 - w1 < ballPos[0] < 900 and y1 < ballPos[1] < y1 + h1:
                    speedX = -speedX
                    ballPos[0] -= 30
                    score[1] += 1
    
    if ballPos[0] < 30 or ballPos[0]>905:
        img = imgGameOver
        if score[0] > score[1]:
            cv2.putText(img, "Left Wins", (300, 220), 
                    cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 0), 3)
            score_fin = str(score[0]).zfill(2)
        elif score[0] < score[1]:
            cv2.putText(img, "Right Wins", (300, 220), 
                    cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 0), 3)
            score_fin = str(score[1]).zfill(2)
        else:
            cv2.putText(img, "Its a draw", (320, 220), 
                    cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 0), 3)
            score_fin = str(score[0]).zfill(2)
            
        cv2.putText(img, score_fin, (440, 330), 
                    cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 0), 3)
    else:
        if ballPos[1] >= 385 or ballPos[1] <= 20:
            speedY = -speedY
                        
        ballPos[0] += speedX
        ballPos[1] += speedY
        
        img = cvzone.overlayPNG(img, pongBall, ballPos)
        cv2.putText(img, str(score[0]), (270, 495), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 0), 3)
        cv2.putText(img, str(score[1]), (700, 495), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 0), 3)
    cv2.imshow("image", img)
    key = cv2.waitKey(1)
    if key == ord('r'):
        ballPos = [150, 50]
        speedX = 7
        speedY = 7
        score = [0,0]
        imgGameOver = cv2.imread("resources/game_over_V2.png")
    if key == ord('q'):
        break
            
print("helo")
    #(480, 640, 3)