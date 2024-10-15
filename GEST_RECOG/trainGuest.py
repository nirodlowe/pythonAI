import cv2
import time
print(cv2.__version__)
import numpy as np
import pickle

class mpHands:
    import mediapipe as mp
    def __init__(self,
                static_image_mode=False,
                max_num_hands=2,
                model_complexity=1,
                min_detection_confidence=0.5,
                min_tracking_confidence=0.5):
     self.hands = self.mp.solutions.hands.Hands(
        static_image_mode=False,
        max_num_hands=2,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    )
    def Marks(self,frame):
        myHands=[]
        frameRGB=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        results=self.hands.process(frameRGB)
        if results.multi_hand_landmarks != None:
            for handLandMarks in results.multi_hand_landmarks:
                myHand=[]
                for landMark in handLandMarks.landmark:
                    myHand.append((int(landMark.x*width),int(landMark.y*height)))
                myHands.append(myHand)
        return myHands
def findDistances(handData):
    distMatrix=np.zeros([len(handData),len(handData)],dtype='float')
    palmSize =np.sqrt((handData[0][0] - handData[9][0])**2 + 
                                  (handData[0][1] - handData[9][1])**2)
    for row in range(0,len(handData)):
        for column in range(0,len(handData)):   #hereby ratio(distance/palmSize) become almost same
           distMatrix[row][column] = (np.sqrt((handData[row][0] - handData[column][0])**2 + 
                                  (handData[row][1] - handData[column][1])**2))/palmSize
   
    return distMatrix
def findError(gestureMatrix,unknownMatrix,keyPoints):
    error=0
    for row in keyPoints:
        for column in keyPoints:
            error=error+abs(gestureMatrix[row][column]-unknownMatrix[row][column])
    return error
def findGestures(unknownGesture,knownGestures,keyPoints,gestures,tol):
    errorArray=[]
    for i in range(0,len(gestNames),1):
        error=findError(knownGestures[i],unknownGesture,keyPoints)
        errorArray.append(error)
    errorMin=errorArray[0]
    minIndex=0
    for i in range(0,len(errorArray)):
        if errorArray[i]<errorMin:
            errorMin=errorArray[i]
            minIndex=i
    if errorMin<tol:
        gesture=gestNames[minIndex]
    if errorMin>=tol:
        gesture='Unknown'
    return gesture   

width=640*2
height=360*2
tol=10
trainCount=0
knownGestures=[]

cam=cv2.VideoCapture(0,cv2.CAP_DSHOW)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT,height)
cam.set(cv2.CAP_PROP_FPS, 30)
cam.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc(*'MJPG'))
findHands=mpHands(2)
time.sleep(5)
keyPoints=[0,4,5,9,13,17,8,12,16,20]

train=int(input('Enter 1 to traise, Enter 0 for recognize: '))
if train==1:
    trainCount=0
    knownGestures=[]
    numGest=int(input('How many gestures u need:  '))
    gestNames=[]
    for i in range(0,numGest):
        prompt='Name of gesture #'+str(i+1)+': '
        name=input(prompt)
        gestNames.append(name)
    print(gestNames)
    trainName=input('file name for train data (Press Enter for default)')
    if trainName=='':
        trainName='default'
    trainName=trainName+'.pkl'

if train==0:
    trainName=input('What Trian Data do u want: (Press Enter for default)')
    if trainName=='':
        trainName='default'
    trainName=trainName+'.pkl'
    with open(trainName,'rb') as f:
        gestNames=pickle.load(f)
        knownGestures=pickle.load(f)

tol=10
while True:
    ignore,  frame = cam.read()
    frame=cv2.resize(frame,(width,height))
    frame = cv2.flip(frame, 1)
    handData=findHands.Marks(frame)
    if train==1:
        if handData!=[]:
            print("Show Your Gesture",gestNames[trainCount], "press t if ready: ")
            if cv2.waitKey(1) & 0xff ==ord('t'):
                knownGesture=findDistances(handData[0])
                knownGestures.append(knownGesture)
                trainCount=trainCount+1
                if trainCount==numGest:
                    train = 0
                    with open(trainName,'wb') as f:
                        pickle.dump(gestNames,f)
                        pickle.dump(knownGestures,f)                                
                
    if train==0:
        if handData!=[]:
            unknownGesture=findDistances(handData[0])
            myGesture=findGestures(unknownGesture,knownGestures,keyPoints,gestNames,tol)
            #error=findError(knownGesture,unknownGesture,keyPoints)
            cv2.putText(frame,myGesture,(100,175),cv2.FONT_HERSHEY_COMPLEX,3,(255,0,0),8)

    for hand in handData:
        for ind in keyPoints:
            cv2.circle(frame,hand[ind],25,(255,0,255),3)
    cv2.imshow('my WEBcam', frame)
    cv2.moveWindow('my WEBcam',0,0)
    if cv2.waitKey(1) & 0xff ==ord('q'):
        break
cam.release()