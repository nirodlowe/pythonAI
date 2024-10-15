import serial
import time
from vpython import*

baseRadius=1
baseHeight=baseRadius/5
bodyRadius=baseRadius*0.75
bodyHeight=baseRadius*2
LEDtopRadius=bodyRadius
LEDtopPos=vector(0,bodyHeight,0)
bulbRadius=bodyRadius*0.75
bulbPos=LEDtopPos
leg1Length=bodyRadius*8
leg2Length=bodyRadius*10
leg3Length=bodyRadius*9
leg4Length=bodyRadius*8
bulbOpacity=0.9
legWidth=baseRadius/10 
topOpacity=bulbOpacity/2
bottomOpacity=bulbOpacity/4
myColor=vector(10,10,10)
myAxis=vector(0,1,0)

LEDbase=cylinder(length=baseHeight,radius=baseRadius,color=myColor,axis=myAxis,opacity=bottomOpacity)
LEDbody=cylinder(length=bodyHeight,radius=bodyRadius,color=myColor,axis=myAxis,opacity=bottomOpacity)
LEDtop=sphere(radius=LEDtopRadius,color=myColor,pos=LEDtopPos,opacity=topOpacity)
bulb=sphere(radius=bulbRadius,coor=myColor,pos=bulbPos,opacity=bulbOpacity)
leg1=box(color=color.white,axis=myAxis,pos=vector(-0.5*baseRadius,-(leg1Length/2)+baseHeight,0),length=leg1Length,width=legWidth,height=legWidth)
leg2=box(color=color.white,axis=myAxis,pos=vector(-0.15*baseRadius,-(leg1Length/2)+baseHeight,0),length=leg2Length,width=legWidth,height=legWidth)
leg3=box(color=color.white,axis=myAxis,pos=vector(0.15*baseRadius,-(leg1Length/2)+baseHeight,0),length=leg3Length,width=legWidth,height=legWidth)
leg4=box(color=color.white,axis=myAxis,pos=vector(0.5*baseRadius,-(leg1Length/2)+baseHeight,0),length=leg4Length,width=legWidth,height=legWidth)
head=compound([bulb,LEDbase,LEDbody,LEDtop])

# Establish serial connection (Update the 'COM3' with your actual port)
arduinoData = serial.Serial('COM3', 9600)  # Set your correct port and baud rate
time.sleep(2)  # Give some time for the connection to establish

# Create a sphere in VPython
# head = sphere(pos=vector(0, 0, 0), radius=1, color=vector(1, 1, 1))

while True:
    if arduinoData.in_waiting > 0:
        try:
            # Read the incoming data from Arduino
            data = arduinoData.readline().decode('ascii').strip()  # Read and decode
            print(f"Received data: {data}")  # Print the received data for debugging
            
            # Split the data based on commas, assuming Arduino sends "xVal,yVal,zVal"
            myColor = data.split(',')
            
            if len(myColor) == 3:  # Ensure there are 3 values
                red = int(myColor[0])
                green = int(myColor[1])
                blue = int(myColor[2])

                

                # Normalize the values to 0-1 for VPython color vectors
                head.color = vector(red/255, green/255, blue/255)
        except Exception as e:
            print(f"Error: {e}")
             
    
    # You can add a small delay to avoid flooding the serial port
    time.sleep(.05)
