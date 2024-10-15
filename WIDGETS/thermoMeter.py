import time
import serial
from vpython import *
import numpy as np
boxX=10
boxY=6
boxZ=.4
offsetRight=boxX/2+2

arduinoData=serial.Serial('com3',9600)
time.sleep(0.5)
scene.center=vector(2.5,0,0)

digValueT=label(text='0',height=20,box=False,pos=vector(0,-4.5,2))
digValueH=label(text='0',height=20,box=False,pos=vector(offsetRight,-4.5,2))
def update_temp():
        digValueT.text = str(str(temp)+"C\nTemperature")
def update_hum():
        digValueH.text = str(str(hum)+"%\nHumidity")

myCase=box(size=vector(boxX,boxY+1,boxZ),color=color.white,pos=vector(offsetRight,boxY/2-3,boxZ/2))
arrowLength=boxY-2
arrowThickness=.15
arrowZoff=.5
myArrow=arrow(length=arrowLength,color=color.red,shaftwidth=arrowThickness,pos=vector(offsetRight,-boxY/4,arrowZoff))

tickL=.4
tickW=.1
tickH=.1
for theta in np.linspace(5*np.pi/6,np.pi/6,11):
    tickMajor=box(pos=vector(arrowLength*np.cos(theta)+offsetRight,arrowLength*np.sin(theta)-boxY/4,arrowZoff),size=vector(tickL,tickW,tickH),color=color.black,axis=vector(arrowLength*np.cos(theta),arrowLength*np.sin(theta),0))
for theta in np.linspace(5*np.pi/6,np.pi/6,51):
    tickMinor=box(pos=vector(arrowLength*np.cos(theta)+offsetRight,arrowLength*np.sin(theta)-boxY/4,arrowZoff),size=vector(tickL*0.5,tickW*0.5,tickH*0.5),color=color.black,axis=vector(arrowLength*np.cos(theta),arrowLength*np.sin(theta),0))
    cnt=0
for theta in np.linspace(5*np.pi/6,np.pi/6,11):
    label=text(text=str(cnt),pos=vector(1.1*arrowLength*np.cos(theta)+offsetRight,1.1*arrowLength*np.sin(theta)-boxY/4,arrowZoff),axis=vector(arrowLength*np.cos(theta-np.pi/2),arrowLength*np.sin(theta-np.pi/2),0),color=color.black,height=.35,align='center')
    cnt=cnt+10

bulb=sphere(radius=1,color=color.red,pos=vector(0,-3,0))
cyl=cylinder(radius=.6,color=color.red,axis=vector(0,1,0),length=6,pos=vector(0,-3,0))
bulbGlass=sphere(radius=1.2,color=color.white,opacity=.25,pos=vector(0,-3,0))
cylBulb=cylinder(radius=.7,color=color.white,opacity=.25,axis=vector(0,1,0),length=6,pos=vector(0,-3,0))

for temp in range(0,115,10):
    tickPos=(4.5/115)*temp+1.5
    tick=cylinder(radius=.7,color=color.black,length=.1,axis=vector(0,1,0),pos=vector(0,tickPos-3,0))
    label=text(text=str(temp),color=color.white,pos=vector(-2,tickPos-3,0),height=.3)
myLabel=text(text='Temperature and Humidity',align='center',color=color.orange,height=boxY/5,pos=vector(boxX-5,0.8*boxY,(-1)*boxZ/2),depth=boxZ)
myLabel=text(text='Hum',align='center',color=color.black,height=boxY/8,pos=vector(offsetRight,-boxY/8,boxZ/2),depth=boxZ/2)
while True:
    while arduinoData.in_waiting==0:
        pass
    dataPacket=arduinoData.readline()
    dataPacket=str(dataPacket,'utf-8')
    dataPacket=dataPacket.strip('\r\n')
    dataPacket=dataPacket.split(',')
    temp=float(dataPacket[0])
    hum=float(dataPacket[1]) 
    len=(4.5/115)*temp+1.5
    cyl.length=len
    update_temp()
    update_hum()
    #digValue.text=str(temp)
    theta=-np.pi/150*hum+5*np.pi/6
    myArrow.axis=vector(arrowLength*np.cos(theta),arrowLength*np.sin(theta),0)

