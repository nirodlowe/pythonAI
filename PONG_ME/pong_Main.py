from vpython import*
import serial
import time
import sys

arduinoData=serial.Serial('com3',9600)

roomX=12
roomY=10
roomZ=16
wallT=.15
wallColor=vector(int(57/255), 1, int(20/255))
wallOpacity=0.8
frontOpacity=0.2
marbleR=0.5
ballColor=vector(1,1,0)
paddleX=3.5
paddleY=3
paddleZ=.2
paddleOpacity=.75
paddleColor=vector(int(125/255), int(249/255), 1)



rChan=1
gChan=1
bChan=0
rInc=0.1
gInc=(-1)*.1
bInc=.1
colorFr=color.blue

myFloor=box(size=vector(roomX,wallT,roomZ),pos=vector(0,-roomY/2,0),color=wallColor,opacity=wallOpacity)
myCeiling=box(size=vector(roomX,wallT,roomZ),pos=vector(0,roomY/2,0),color=wallColor,opacity=wallOpacity)
myLwal=box(size=vector(wallT,roomY,roomZ),pos=vector(roomX/2,0,0),color=wallColor,opacity=wallOpacity)
myRwal=box(size=vector(wallT,roomY,roomZ),pos=vector(-roomX/2,0,0),color=wallColor,opacity=wallOpacity)
myBackWall=box(size=vector(roomX,roomY,wallT),pos=vector(0,0,-roomZ/2),color=wallColor,opacity=wallOpacity)
myFrontWall=box(size=vector(roomX,roomY,wallT),pos=vector(0,0,roomZ/2),color=colorFr,opacity=frontOpacity)
marble=sphere(color=ballColor,radius=marbleR)
paddle=box(size=vector(paddleX,paddleY,paddleZ),pos=vector(0,0,roomZ/2),color=paddleColor,opacity=paddleOpacity)

num_lines = 10  # Number of grid lines
grid_color = color.black  # Color for the gridlines

# Draw gridlines parallel to the X-axis
for i in range(num_lines):
    offset = (i / (num_lines - 1)) * roomZ - (roomZ / 2)
    curve(pos=[vector(-roomX / 2, -roomY/2, offset), vector(roomX / 2, -roomY/2, offset)], color=grid_color)
for i in range(num_lines):
    offset = (i / (num_lines - 1)) * roomZ - (roomZ / 2)
    curve(pos=[vector(-roomX / 2, roomY/2, offset), vector(roomX / 2, roomY/2, offset)], color=grid_color)
for i in range(num_lines):
    offset = (i / (num_lines - 1)) * roomZ - (roomZ / 2)
    curve(pos=[vector(-roomX / 2, -roomY / 2, offset), vector(-roomX / 2, roomY / 2, offset)], color=grid_color)
for i in range(num_lines):
    offset = (i / (num_lines - 1)) * roomZ - (roomZ / 2)
    curve(pos=[vector(roomX / 2, -roomY / 2, offset), vector(roomX / 2, roomY / 2, offset)], color=grid_color)
for i in range(num_lines):
    offset = (i / (num_lines - 1)) * roomX - (roomX / 2)
    curve(pos=[vector(offset, -roomY / 2, -roomZ / 2), vector(offset, roomY / 2, -roomZ / 2)], color=grid_color)

marbleX=0
marbleY=0
marbleZ=0

deltaX=0.1
deltaY=0.1
deltaZ=0.1

score=0
lives=3

while True:
    
    while arduinoData.in_waiting==0:
        pass
    dataPacket=arduinoData.readline()
    dataPacket=str(dataPacket,'utf-8')
    dataPacket.strip('\r\n')
    splitPacket=dataPacket.split(',')

    x=float(splitPacket[0])
    y=float(splitPacket[1])
    z=float(splitPacket[2])

    padX=(roomX/1023.0)*x-(roomX/2)
    padY=-(roomY/1023.0)*y+(roomY/2)
   
    rChan=rChan+rInc
    gChan=gChan+gInc
    bChan=bChan+bInc

    if rChan<=1:
        rApply=rChan
    if rChan>1:
        rApply=1
    
    if gChan<=1:
        gApply=gChan
    if gChan>1:
        gApply=1

    if bChan<=1:
        bApply=bChan
    if bChan>1:
        bApply=1

    marbleX=marbleX+deltaX
    marbleY=marbleY+deltaY
    marbleZ=marbleZ+deltaZ
    if ((marbleX+marbleR)>=(roomX/2-wallT/2)) or ((marbleX-marbleR)<=(-roomX/2+wallT/2)):
        deltaX=-deltaX
        marbleX=marbleX+deltaX
        marble.color=vector(rApply,gApply,bApply)
    if ((marbleY-marbleR)<=(-roomY/2+wallT/2)) or ((marbleY+marbleR)>=(roomY/2-wallT/2)):
        deltaY=-deltaY
        marbleY=marbleY+deltaY
        marble.color=vector(rApply,gApply,bApply)
    if ((marbleZ-marbleR)<=(-roomZ/2+wallT/2)) :
        deltaZ=-deltaZ
        marbleZ=marbleZ+deltaZ
        marble.color=vector(rApply,gApply,bApply)
    if marbleZ+marbleR>=roomZ/2-wallT/2:
        if marbleX>padX-paddleX/2 and marbleX<padX+paddleX/2 and marbleY>padY-paddleY/2 and marbleY<padY+paddleY/2:
            score=score+1
            deltaZ=deltaZ*(-1)
            marbleZ=marbleZ+deltaZ
        else:
            lives=lives-1
            time.sleep(1)
            
            marbleX=0
            marbleY=0
            marbleZ=0
        if lives==0:
            lbl=label(text='Game Over',height=15,font="serif")
            time.sleep(2)
            sys.exit()

    lbl=label(text='Scoe: '+str(score),pos=vector(roomX/2, roomY/2, roomZ/2))
    lbl=label(text='Lives: '+str(lives),pos=vector(roomX/2, roomY/4, roomZ/2))   
    marble.pos=vector(marbleX,marbleY,marbleZ)
    paddle.pos=vector(padX,padY,roomZ/2)

    if rChan>=1.5 or rChan<=0:
        rInc=(-1)*rInc
    if gChan>=1.5 or gChan<=0:
        gInc=(-1)*gInc
    if bChan>=1.5 or bChan<=0:
        bInc=(-1)*bInc
    
    pass