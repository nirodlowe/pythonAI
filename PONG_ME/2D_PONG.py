import cv2
import time
print(cv2.__version__)

class mpHands:
    import mediapipe as mp
    def __init__(self,maxHands=2,tol1=int(.5),tol2=int(.5)):
        self.hands=self.mp.solutions.hands.Hands(False,maxHands,tol1,tol2)
    def Marks(self,frame):
        myHands=[]
        handsType=[]
        frameRGB=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        results=self.hands.process(frameRGB)
        if results.multi_hand_landmarks != None:
            #print(results.multi_handedness)
            for hand in results.multi_handedness:
                #print(hand)
                #print(hand.classification)
                #print(hand.classification[0])
                handType=hand.classification[0].label
                handsType.append(handType)
            for handLandMarks in results.multi_hand_landmarks:
                myHand=[]
                for landMark in handLandMarks.landmark:
                    myHand.append((int(landMark.x*width),int(landMark.y*height)))
                myHands.append(myHand)
        return myHands,handsType

width=1280
height=720
cam=cv2.VideoCapture(0,cv2.CAP_DSHOW)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT,height)
cam.set(cv2.CAP_PROP_FPS, 30)
cam.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc(*'MJPG'))
findHands=mpHands(2)

padWidth=25
padHeigth=125
padColorL=(0,0,255)
padColorR=(255,0,0)
boundColor= (210, 105, 30)
ballRadius=25
ballColor=(255,0,255)
xPos=int(width/2)
yPos=int(height/2)
deltaX=3
deltaY=3
font=cv2.FONT_HERSHEY_SIMPLEX
fontHeight=5
fontWeight=5
font = cv2.FONT_HERSHEY_SIMPLEX
font1=cv2.FONT_HERSHEY_SIMPLEX
font2=cv2.FONT_HERSHEY_COMPLEX
fontColor=(0,0,0)
line_color=(0,255,0)
yLefttip=0
yRighttip=0
scoreLeft=0
scoreRight=0
offset=8

while True:
    ignore,  frame = cam.read()
    frame=cv2.resize(frame,(width,height))
    frame = cv2.flip(frame, 1)
    cv2.circle(frame,(xPos,yPos),ballRadius,ballColor,-1)

    # Draw the center dividing line (dotted)
    for i in range(0, height, 20):
        cv2.line(frame, (width // 2, i), (width // 2, i + 10), line_color, 2)
    
    cv2.putText(frame, 'SL', (int(width/2 - 100), 50), font, 2, padColorL, 3, cv2.LINE_AA)
    cv2.putText(frame, str(scoreLeft), (int(width/2 - 100), 95), font, 2, line_color, 3, cv2.LINE_AA)
    cv2.putText(frame, 'AUS', (int(width/2 + 50), 50), font, 2, padColorR, 3, cv2.LINE_AA)
    cv2.putText(frame, str(scoreRight), (int(width/2 + 50), 95), font, 2, line_color, 3, cv2.LINE_AA)
    handData, handsType=findHands.Marks(frame)
    for hand,handType in zip(handData,handsType):
        if handType=='Right':
            handColor=(255,0,0)
        if handType=='Left':
            handColor=(0,0,255)
        for ind in [0,5,6,7,8]:
            cv2.circle(frame,hand[ind],15,handColor,5)
        if handType=='Left':
            yLefttip=hand[8][1]
        if handType=='Right':
            yRighttip=hand[8][1]
        
    cv2.rectangle(frame,(0,int(yLefttip-(padHeigth/2))),(padWidth,int(yLefttip+(padHeigth/2))),padColorL,-1)
    cv2.rectangle(frame,(width-padWidth,int(yRighttip-(padHeigth/2))),(width,int(yRighttip+(padHeigth/2))),padColorR,-1)

    cv2.rectangle(frame,(0,0),(width,offset),boundColor,-1)
    cv2.rectangle(frame,(0,height-offset),(width,height),boundColor,-1)   

    topEdg=yPos-ballRadius
    botEdg=yPos+ballRadius
    leftEdg=xPos-ballRadius
    rightEdg=xPos+ballRadius

    if topEdg<=0:
        deltaY=(-1)*deltaY
    if botEdg>=height:
        deltaY=(-1)*deltaY
    if leftEdg<=padWidth:
        if yPos>=int(yLefttip-(padHeigth/2)) and yPos<=int(yLefttip+(padHeigth/2)):
            deltaX=(-1)*deltaX
            scoreLeft=scoreLeft+1
        else:
            xPos=int(width/2)
            yPos=int(height/2)
            scoreRight=scoreRight+1

    if rightEdg>=width-padWidth:
        if yPos>=int(yRighttip-(padHeigth/2)) and yPos<=int(yRighttip+(padHeigth/2)):
            deltaX=(-1)*deltaX
            scoreRight=scoreRight+1
        else:
            xPos=int(width/2)
            yPos=int(height/2)
            scoreLeft=scoreLeft+1

    xPos=xPos+deltaX
    yPos=yPos+deltaY
    if scoreLeft+scoreRight>=5:
        break

    cv2.imshow('my WEBcam', frame)
    cv2.moveWindow('my WEBcam',0,0)
    if cv2.waitKey(1) & 0xff ==ord('q'):
        break
cam.release()