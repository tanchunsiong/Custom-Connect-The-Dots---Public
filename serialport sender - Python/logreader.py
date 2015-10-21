﻿
import sys
import re
import time
import datetime
import os
import serial
from azure.servicebus import ServiceBusService


key_name = "linuxlogger"
key_value = "SdcLrzfc7JMq5Ny+s972ydTwwU98DMBp6slwTXLGx68="

sbs = ServiceBusService("cspi1-ns",shared_access_key_name=key_name, shared_access_key_value=key_value)

try:
   
    #logfile = raw_input("Please enter a file to parse, e.g /var/log/secure: ")
    #logfile ="/var/log/secure"
    logfile ="secure"
    ser = serial.Serial('COM7', 9600)
    #ser = serial.Serial('/dev/ttyACM0', 9600)
    while(True):
        try:
            text = ser.readline()
            thisRunWaterMark=datetime.datetime.now()
            timecreated=thisRunWaterMark.strftime("%Y-%m-%dT%H:%M:%S.0000000Z")
            if '}' in text:
              firststring= text.split('timenow')[0];
              laststring= text.split('timenow')[1];
              messagetosend = firststring + timecreated  +laststring;
              print(messagetosend);
              sbs.send_event('ehdevices',messagetosend);
              text='';

        except Exception as ex:
            template = "An exception of type {0} occured, Arguments : {1!r}"
            message = template.format(type(ex).__name__,ex.args)
            print message
except:
        print "I/O Error"



