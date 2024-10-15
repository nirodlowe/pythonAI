from vpython import*
import numpy as np
import time

ClockR=2
ClockT=ClockR/10

majorTickL=ClockR/7
majorTickT=2*np.pi*ClockR/250
majorTickW=ClockT

minorTickL=ClockR/12
minorTickT=2*np.pi*ClockR/600
minorTickW=ClockT

minHandL=ClockR-(majorTickL)
minHandT=minHandL/30
minHandOffset=ClockT/2+minHandT

secHandL=ClockR-(majorTickL/2)
secHandT=minHandL/50
secHandOffset=ClockT/1.5+minHandT

hrHandL=minHandL*0.65
hrHandT=minHandT*2
hrHandOffset=ClockT/2+minHandT

hubRadius=ClockT*0.5
hubLength=ClockT*1.1

minInc=0.0001
hrInc=minInc/12
secInc=minInc*60


for theta in np.linspace(0,2*np.pi,13):
    majorTick=box(axis=vector(ClockR*np.cos(theta),ClockR*np.sin(theta),0),color=color.black,length=majorTickL,width=majorTickW,height=majorTickT,pos=vector((ClockR-majorTickL/2)*np.cos(theta),(ClockR-majorTickL/2)*np.sin(theta),0.01))
for theta in np.linspace(0,2*np.pi,61):
    minorTick=box(axis=vector(ClockR*np.cos(theta),ClockR*np.sin(theta),0),color=color.black,length=minorTickL,width=minorTickW,height=minorTickT,pos=vector((ClockR-minorTickL/2)*np.cos(theta),(ClockR-minorTickL/2)*np.sin(theta),0.01))

secHand=arrow(axis=vector(0,1,0),color=color.red,shaftwidth=secHandT,length=secHandL,pos=vector(0,0,secHandOffset))
minHand=arrow(axis=vector(0,1,0),color=color.red,shaftwidth=minHandT,length=minHandL,pos=vector(0,0,minHandOffset))
hrHand=arrow(axis=vector(1,0,0),color=color.red,shaftwidth=hrHandT,length=hrHandL,pos=vector(0,0,hrHandOffset))
ClockFace=cylinder(axis=vector(0,0,1),color=vector(0,1,1),length=ClockT,radius=ClockR,pos=vector(0,0,-ClockT/2))
hub=cylinder(axis=vector(0,0,1),color=color.red,radius=hubRadius,length=hubLength)
myLabel=text(text='Colombo Time',align='center',color=color.orange,height=ClockR/4,pos=vector(0,1.1*ClockR,(-1)*ClockT/2),depth=ClockT)
Angle=np.pi/2
AngleInc=-2*np.pi/12
Angle=Angle+AngleInc
numH=ClockR/7
for i in range(1,13,1):
    clockNum=text(align='center',text=str(i),pos=vector(ClockR*0.75*np.cos(Angle),ClockR*0.75*np.sin(Angle)-numH/2,0),height=numH,depth=ClockT,color=color.orange)
    Angle=Angle+AngleInc
time_display = label(pos=vector(0, -ClockR-0.5, 0), text='', height=20, color=color.white, box=False)
while True:
    rate(5000)
    hour=time.localtime(time.time())[3]
    if hour>12:
        hour=hour-12
    minute=time.localtime(time.time())[4]
    if minute>60:
        minute=minute-60
    second=time.localtime(time.time())[5]
    
    secAngle=((second/60)*np.pi*2*-1)+np.pi*(0.5)
    minAngle=(((minute+(second/60))/60)*np.pi*2*-1)+np.pi*(0.5)
    hrAngle=(((hour+(minute/60))/12)*np.pi*2*-1)+np.pi*(0.5)
    print(hour,'\t',minute,'\t',second)


    hrHand.axis=vector(hrHandL*np.cos(hrAngle),hrHandL*np.sin(hrAngle),0)
    minHand.axis=vector(minHandL*np.cos(minAngle),minHandL*np.sin(minAngle),0)
    secHand.axis=vector(secHandL*np.cos(secAngle),secHandL*np.sin(secAngle),0)

    current_time = time.strftime("%H:%M:%S", time.localtime())
    time_display.text = current_time
    rate(1)

    pass