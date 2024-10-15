import cv2
import time
print(cv2.__version__)
width = 640
height = 360
video_path = 'C://Users\ASUS\Documents\PythonMark\OFFICE_COUNTER\WOLF.mp4'  # Specify the path to your video file here
cam = cv2.VideoCapture(video_path)

cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

faceCascade=cv2.CascadeClassifier('haar\haarcascade_frontalface_default.xml')
eyeCascade=cv2.CascadeClassifier('haar\haarcascade_eye.xml')
# eyeGlassCascade=cv2.CascadeClassifier('haar\haarcascade_frontalcatface.xml')
fps=10
timeStamp=time.time()
while True:
    ignore,  frame = cam.read()
    frameGray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    faces=faceCascade.detectMultiScale(frameGray,1.3,5)
    i=0
    for face in faces:
        x,y,w,h=face
        cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),3)
        i=i+1
        # print(i)
        frameROI=frame[y:y+h,x:x+w]
        frameROIGray=cv2.cvtColor(frameROI,cv2.COLOR_BGR2GRAY)
        eyes=eyeCascade.detectMultiScale(frameROIGray)
        # eyesG=eyeGlassCascade.detectMultiScale(frameROIGray)
        for eye in eyes:
            xEye,yEye,wEye,hEye=eye
            cv2.rectangle(frame[y:y+h,x:x+w],(xEye,yEye),(xEye+wEye,yEye+hEye),(0,255,0),3)
        # for eyeG in eyesG:
        #     xEye,yEye,wEye,hEye=eyeG
        #     cv2.rectangle(frame[y:y+h,x:x+w],(xEye,yEye),(xEye+wEye,yEye+hEye),(0,255,0),3)

    loopTime=time.time()-timeStamp
    timeStamp=time.time()
    fpsNew=1/loopTime
    fps=0.9*fps+.1*fpsNew
    fps=int(fps)
    # print(fps)
    cv2.putText(frame,'FPS: '+str(fps),(5,30),cv2.FONT_HERSHEY_PLAIN,1.5,(0,0,255),2)
    cv2.putText(frame,'COUNT: '+str(i),(5,50),cv2.FONT_HERSHEY_PLAIN,1.5,(0,0,255),2)
    cv2.imshow('my WEBcam', frame)
    cv2.moveWindow('my WEBcam',0,0)
    if cv2.waitKey(1) & 0xff ==ord('q'):
        break
cam.release()