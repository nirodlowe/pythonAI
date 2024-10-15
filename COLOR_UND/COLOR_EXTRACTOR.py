import cv2
import numpy as np
print(cv2.__version__)

def onTrack1(val):
    global hueLow
    print('Hue Low is ',hueLow)
    hueLow=val
def onTrack2(val):
    global hueHigh
    print('Hue High is ',hueHigh)
    hueHigh=val
def onTrack3(val):
    global satLow
    print('Sat Low is ',satLow)
    satLow=val
def onTrack4(val):
    global satHigh
    print('Sat High is ',satHigh)
    satHigh=val
def onTrack5(val):
    global valLow
    print('Val Low is ',valLow)
    valLow=val
def onTrack6(val):
    global valHigh
    print('Val High is ',valHigh)
    valHigh=val

def onTrack7(val):
    global hueLow2
    print('Hue Low2 is ',hueLow2)
    hueLow2=val
def onTrack8(val):
    global hueHigh2
    print('Hue High2 is ',hueHigh2)
    hueHigh2=val

width=640
height=360
cam=cv2.VideoCapture(0,cv2.CAP_DSHOW)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT,height)
cam.set(cv2.CAP_PROP_FPS, 30)
cam.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc(*'MJPG'))

cv2.namedWindow('my Tracker')
cv2.resizeWindow('my Tracker',width,height)
cv2.moveWindow('my Tracker',width,0)

hueLow=10
hueHigh=20
hueLow2=10
hueHigh2=20
satLow=10
satHigh=250
valLow=10
valHigh=250

cv2.createTrackbar('Hue Low','my Tracker',10,179,onTrack1)
cv2.createTrackbar('Hue High','my Tracker',10,179,onTrack2)
cv2.createTrackbar('Sat Low','my Tracker',10,255,onTrack3)
cv2.createTrackbar('Sat High','my Tracker',10,255,onTrack4)
cv2.createTrackbar('Val Low','my Tracker',10,255,onTrack5)
cv2.createTrackbar('Val High','my Tracker',250,255,onTrack6)

cv2.createTrackbar('Hue Low2','my Tracker',10,179,onTrack7)
cv2.createTrackbar('Hue High2','my Tracker',10,179,onTrack8)

while True:
    ignore,  frame = cam.read()
    frameHSV=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    lowerBound=np.array([hueLow,satLow,valLow])
    upperBound=np.array([hueHigh,satHigh,valHigh])

    lowerBound2=np.array([hueLow2,satLow,valLow])
    upperBound2=np.array([hueHigh2,satHigh,valHigh])

    myMask=cv2.inRange(frameHSV,lowerBound,upperBound)
    myMask2=cv2.inRange(frameHSV,lowerBound2,upperBound2)
    myCompMask=myMask|myMask2   

    #myMask=cv2.bitwise_not(myMask)
    myObj=cv2.bitwise_and(frame,frame,mask= myCompMask)
    myObjSmall=cv2.resize(myObj,(int(width/2),int(height/2)))
    cv2.imshow('My Obj',myObj)
    cv2.moveWindow('My Obj',int(width),int(height+80))
    cv2.imshow('My Mask',myMask)
    cv2.imshow('My Mask2',myMask2)

    myMaskSmall=cv2.resize(myMask,(int(width/2),int(height/2)))
    myMaskSmall2=cv2.resize(myMask2,(int(width/2),int(height/2)))
    cv2.moveWindow('My Mask',0,int(height+80))
    cv2.moveWindow('My Mask2',width,int(height+80))
    cv2.imshow('my WEBcam', frame)
    cv2.moveWindow('my WEBcam',0,0)
    if cv2.waitKey(1) & 0xff ==ord('q'):
        break
cam.release()