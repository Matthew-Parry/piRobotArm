# -*- coding: utf-8 -*-
# Scratch Robot Arm handler by Matthew Parry 2013
#
# ScratchSender and ScratchListener classes dervived from scratch_gpio_handler 
# written by Simon Walters

from array import *
import threading
import sys
import struct
import socket
import time
import usb.core
import usb.util

PORT = 42001
DEFAULT_HOST = '127.0.0.1'
BUFFER_SIZE = 240 
SOCKET_TIMEOUT = 1

import scratch
s = scratch.Scratch()

#allocate the name 'RoboArm' to the USB device
RoboArm=usb.core.find(idVendor=0x1267,idProduct=0x0000)

#Check to see if arm is detected
if RoboArm is None:
     raise ValueError("Arm not found")

#Create a variable for duration
Duration=0.05

#Define a procedure to execute each arm movement
def MoveArm(Duration, ArmCmd):
     #start the movement
     RoboArm.ctrl_transfer(0x40,6,0x100,0,ArmCmd,1000)
     #stop the movement atfer specified duration
     time.sleep(Duration)
     ArmCmd=(0,0,0)
     RoboArm.ctrl_transfer(0x40,6,0x100,0,ArmCmd,1000)

     
# to make a broadcast to scratch
#s.broadcast("from python")



class ScratchSender(threading.Thread):
    def __init__(self, socket):
        threading.Thread.__init__(self)
        self.scratch_socket = socket
        self._stop = threading.Event()

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()

    def run(self):
         while not self.stopped():
            time.sleep(1.1) # be kind to cpu - not certain why :)




class ScratchListener(threading.Thread):
    def __init__(self, socket):
        threading.Thread.__init__(self)
        self.scratch_socket = socket
        self._stop = threading.Event()

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()

    def run(self):
        global cycle_trace
        #This is main listening routine
        while not self.stopped():
          try:

               # to receive an update from scratch
               message = s.receive()
               print(message)

               # blocks until an update is received
               # message returned as  {'broadcast': [], 'sensor-update': {'scratchvar': '64'}}
               #                  or  {'broadcast': ['from scratch'], 'sensor-update': {}}
               # where scratchvar is the name of a variable in scratch
               # and 'from scratch' is the name of a scratch broadcast

               # send sensor updates to scratch
               #data = {}
               #data['pyvar'] = 123
               #for data['pycounter'] in range(60):
               #    s.sensorupdate(data)

               msgtype = message#['broadcast']    #'broadcast'
               #print msgtype

          except socket.timeout:
                     print "No data received: socket timeout"
                     continue

                   
          #move arm as per broadcast message
          if 'elbowup' in msgtype:
               MoveArm(1,[16,0,0]) #elbow up
          if 'elbowdown' in msgtype:
               MoveArm(1,[32,0,0]) #elbow down
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

          if 'stop handler' in msgtype:
               cycle_trace = 'disconnected'
               break
                #cleanup_threads((listener, sender))
                #sys.exit()


def create_socket(host, port):
    while True:
        try:
            print 'Trying'
            scratch_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            scratch_sock.connect((host, port))
            break
        except socket.error:
            print "There was an error connecting to Scratch!"
            print "I couldn't find a Mesh session at host: %s, port: %s" % (host, port) 
            time.sleep(3)
            #sys.exit(1)

    return scratch_sock

def cleanup_threads(threads):
    for thread in threads:
        thread.stop()

    for thread in threads:
        thread.join()

if __name__ == '__main__':
    if len(sys.argv) > 1:
        host = sys.argv[1]
    else:
        host = DEFAULT_HOST


cycle_trace = 'start'
while True:

    if (cycle_trace == 'disconnected'):
        print "Scratch disconnected"
        cleanup_threads((listener, sender))
        time.sleep(1)
        cycle_trace = 'start'

    if (cycle_trace == 'start'):
        # open the socket
        print 'Starting to connect...' ,
        the_socket = create_socket(host, PORT)
        print 'Connected!'
        the_socket.settimeout(SOCKET_TIMEOUT)
        listener = ScratchListener(the_socket)
        sender = ScratchSender(the_socket)
        cycle_trace = 'running'
        print "Running...."
        listener.start()
        sender.start()

    # wait for ctrl+c
    try:
        time.sleep(0.5)
    except KeyboardInterrupt:
        cleanup_threads((listener,sender))
        sys.exit()
