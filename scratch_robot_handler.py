# -*- coding: utf-8 -*-
# Scratch Robot Arm handler by Matthew Parry 2013
#
# based on code written by Simon Walters
# 


import socket
import time
import string
import usb.core
import usb.util

import scratch
s = scratch.Scratch()

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

     
# to make a broadcast to scratch
#s.broadcast("from python")


#need to poll for msgs from scratch and end when comms killed by scratch ...

# to receive an update from scratch
message = s.receive()
print message


# blocks until an update is received
# message returned as  {'broadcast': [], 'sensor-update': {'scratchvar': '64'}}
#                  or  {'broadcast': ['from scratch'], 'sensor-update': {}}
# where scratchvar is the name of a variable in scratch
# and 'from scratch' is the name of a scratch broadcast

# send sensor updates to scratch
data = {}
data['pyvar'] = 123
for data['pycounter'] in range(60):
    s.sensorupdate(data)


msgtype = message['broadcast']    #'broadcast'
#msgcommand = message.   #'from scratch'

print msgtype

    
#elbow up
if 'elbowup' in msgtype:
    MoveArm(1,[16,0,0]) #elbow up
if 'elbowdown' in msgtype:
     MoveArm(1,[32,0,0]) #elbow down
     
#Give arm some commands
if 'baseanticlockwise' in msgtype:
     MoveArm(1,[0,1,0]) #rotate base anti-clockwise
if 'baseclockwise' in msgtype:
     MoveArm(1,[0,2,0]) #rotate base clockwise
if 'shoulderup' in msgtype:
     MoveArm(1,[64,0,0]) #shoulder up
if 'shoulderdown' in msgtype:
     MoveArm(1,[128,0,0]) #shoulder down
if 'wristup' in msgtype:
     MoveArm(1,[4,0,0]) #wrist up
if 'wristdown' in msgtype:
     MoveArm(1,[8,0,0]) #wrist down
if 'gripopen' in msgtype:
     MoveArm(1,[2,0,0]) #grip open
if 'gripclose' in msgtype:
     MoveArm(1,[1,0,0]) #grip closed
if 'lighton' in msgtype:
     MoveArm(1,[0,0,1]) #light on
if 'lightoff' in msgtype:
     MoveArm(1,[0,0,0]) #light off




