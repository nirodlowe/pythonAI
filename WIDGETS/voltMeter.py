import time
import serial
from vpython import*
import numpy as np
ardData=serial.Serial('com3',9600)
time.sleep(1)

arrowLength=1
arrowWidth=.02
myArrow=arrow(lenght=arrowLength,shaftwidth=arrowWidth,color=color.red)
hubL=.05
hubR=.05
hub=cylinder(color=color.red,radius=hubR,length=hubL,axis=vector(0,0,-1))
tickL=.1
tickW=.02
tickH=.02

for theta in np.linspace(5*np.pi/6,np.pi/6,6):
    tickMajor=box(color=color.black,pos=vector(arrowLength*np.cos(theta),arrowLength*np.sin(theta),0),size=vector(tickL,tickW,tickH),axis=vector(arrowLength*np.cos(theta),arrowLength*np.sin(theta),0))
for theta in np.linspace(5*np.pi/6,np.pi/6,51):
    tickMinor=box(color=color.black,pos=vector(arrowLength*np.cos(theta),arrowLength*np.sin(theta),0),size=vector(tickL*0.5,tickW*0.5,tickH*0.5),axis=vector(arrowLength*np.cos(theta),arrowLength*np.sin(theta),0))
cnt=0
labF=1.1
for theta in np.linspace(5*np.pi/6,np.pi/6,6):
    lab=text(text=str(cnt),pos=vector(labF*arrowLength*np.cos(theta),labF*arrowLength*np.sin(theta),0),color=color.black,height=0.1,align='center',axis=vector(arrowLength*np.cos(theta-(np.pi/2)),arrowLength*np.sin(theta-(np.pi/2)),0))
    cnt=cnt+1

boxX=2.5
boxY=1.75
boxZ=0.1
offsetRight=boxX/2+2
myCase=box(color=color.white,size=vector(boxX,boxY,boxZ),pos=vector(0,0.45*boxY,-boxZ))

myLabel=text(text='voltOmatic',pos=vector(0,1.3,0),color=color.red,height=.25,align='center')
myLabel=text(text='V',align='center',color=color.black,height=boxY/8,pos=vector(0,boxY/8,0),depth=boxZ/2)
digValueT=label(text='0',height=20,box=False,pos=vector(0,-0.5,0))
while True:
    while (ardData.inWaiting()==0):
        pass
    dataPacket=ardData.readline()
    dataPacket=str(dataPacket,'utf-8')
    dataPacket=int(dataPacket.strip('\r\n'))
    potVal=dataPacket
    theta=(-2*np.pi/3069)*potVal+5*np.pi/6
    myArrow.axis=vector(arrowLength*np.cos(theta),arrowLength*np.sin(theta),0)
    convVal=round(potVal*(5/1023),1)
    print(convVal)
    digValueT.text = str(str(convVal)+"V\nVoltage")
    # digValueH=label(text='0',height=20,box=False,pos=vector(offsetRight,-4.5,2))
    # for theta in np.linspace(5*np.pi/6,np.pi/6,150):
    #     rate(25)
    #     myArrow.axis=vector(arrowLength*np.cos(theta),arrowLength*np.sin(theta),0)
    # for theta in np.linspace(np.pi/6,5*np.pi/6,150):
    #     rate(25)
    #     myArrow.axis=vector(arrowLength*np.cos(theta),arrowLength*np.sin(theta),0)
    
   

