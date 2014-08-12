#!/usr/bin/env python

#import the USB abd time libraries
import usb.core, usb.util, time

#allocate the name 'RoboArm' to the USB device
RoboArm=usb.core.find(idVendor=0x1267,idProduct=0x0000)

#Check to see if arm is detected
if RoboArm is None:
     raise ValueError("Arm not found")

#Create a variable for duration
Duration=1

#Define a procedure to execute each movement
def MoveArm(Duration, ArmCmd):
     #start the movement
     RoboArm.ctrl_transfer(0x40,6,0x100,0,ArmCmd,1000)
     #stop the movement atfer specified duration
     time.sleep(Duration)
     ArmCmd=(0,0,0)
     RoboArm.ctrl_transfer(0x40,6,0x100,0,ArmCmd,1000)

#Give arm some commands
MoveArm(1,[0,1,0]) #rotate base anti-clockwise
MoveArm(1,[0,2,0]) #rotate base clockwise
MoveArm(1,[64,0,0]) #shoulder up
MoveArm(1,[128,0,0]) #shoulder down
MoveArm(1,[16,0,0]) #elbow up
MoveArm(1,[32,0,0]) #elbow down
MoveArm(1,[4,0,0]) #wrist up
MoveArm(1,[8,0,0]) #wrist down
MoveArm(1,[2,0,0]) #grip open
MoveArm(1,[1,0,0]) #grip closed
MoveArm(1,[0,0,1]) #light on
MoveArm(1,[0,0,0]) #light off





