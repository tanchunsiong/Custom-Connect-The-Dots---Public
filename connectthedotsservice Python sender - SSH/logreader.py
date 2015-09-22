#<standard shebang line>
#fixed the import, just red PEP 8
import sys
import re
import time
import datetime
import os
import threading
from multiprocessing import Pool
from azure.servicebus import ServiceBusService

key_name = "eventhub key name"
key_value = "eventhubkey"

sbs = ServiceBusService("cspi1-ns",shared_access_key_name=key_name, shared_access_key_value=key_value)

try:
    if sys.argv[1:]:
        print "File: %s" % (sys.argv[1])
        logfile = sys.argv[1]
        
    else:
        #logfile = raw_input("Please enter a file to parse, e.g /var/log/secure: ")
        logfile ="/var/log/secure"
    while(True):
        lastRunWaterMark=datetime.datetime.now()
        thisRunWaterMark=datetime.datetime.now()
        isfirstrun=0
        isfirstrunRepeat=1
        count=0
        try:
            timefile = open("last_time_processed", "r")   
          
            for text in timefile.readlines():
                    lastRunWaterMark=datetime.datetime.strptime(text,"%Y-%m-%dT%H:%M:%S")
        except:
             #lastRunWaterMark =datetime.datetime.now()
             isfirstrun=1
        try:

            file = open(logfile, "r")
            for text in reversed(file.readlines()):
               if count >=20:
                   break;
               try:
                   text = text.rstrip()
                   timecreated= datetime.datetime.strptime(text[:19],"%Y-%m-%dT%H:%M:%S")
                   if isfirstrun == 1 :
                       if isfirstrunRepeat == 1 :
                           thisRunWaterMark=timecreated
                           isfirstrunRepeat=0
                       #greedy run first
                       outfile = open("last_time_processed", "w")
                       outfile.write(thisRunWaterMark.strftime("%Y-%m-%dT%H:%M:%S"))
                       outfile.close()
                       #run until end 
                       if 'reverse mapping checking getaddrinfo for' in text:
                        count+=1 
                        dns= text.split('for ')[1].split(' [')[0]
                        ip= text.split('for ')[1].split(' failed')[0].split('[')[1].split(']')[0]
                        messagetosend = '{"guid":"62X74059-A444-4797-8A7E-526C3EF9D64B","organization":"SG MIC","timecreated":"'+timecreated.strftime("%Y-%m-%dT%H:%M:%S.0000000Z")+'","displayname":"SSH Sensor","location":"Azure DC Singapore","measurename":"SSH Reverse Mapping","unitofmeasure":"count","value":1,"dns":"'+dns+'","ip":"'+ip+'"}'
                        print('sending event at ' +messagetosend)
                        sbs.send_event('ehdevices', messagetosend)
                        
                       elif 'Failed password for root' in text:
                        count+=1 
                        ip= text.split('from ')[1].split(' port')[0]
                        port= text.split('port ')[1].split(' ssh')[0]
                        messagetosend = '{"guid":"62X74059-A444-4797-8A7E-526C3EF9D64B","organization":"SG MIC","timecreated":"'+timecreated.strftime("%Y-%m-%dT%H:%M:%S.0000000Z")+'","displayname":"SSH Sensor","location":"Azure DC Singapore","measurename":"SSH Failed Login Attempt","unitofmeasure":"count","value":1,"port":"'+port+'","ip":"'+ip+'"}'
                        print('sending event at ' +messagetosend)
                        sbs.send_event('ehdevices', messagetosend)
                       elif 'Failed password for invalid user' in text:
                        count+=1 
                        ip= text.split('from ')[1].split(' port')[0]
                        port= text.split('port ')[1].split(' ssh')[0]
                        user = text.split('user ')[1].split(' from')[0]
                        messagetosend = '{"guid":"62X74059-A444-4797-8A7E-526C3EF9D64B","organization":"SG MIC","timecreated":"'+timecreated.strftime("%Y-%m-%dT%H:%M:%S.0000000Z")+'","displayname":"SSH Sensor","location":"Azure DC Singapore","measurename":"SSH Failed Login Attempt","unitofmeasure":"count","value":1,"port":"'+port+'","ip":"'+ip+'","user":"'+user+'"}'
                        print('sending event at ' +messagetosend)
                        sbs.send_event('ehdevices', messagetosend) 
                       elif 'Did not receive identification string' in text:
                        count+=1   
                        ip = text.split('from ')[1]
                        messagetosend = '{"guid":"62X74059-A444-4797-8A7E-526C3EF9D64B","organization":"SG MIC","timecreated":"'+timecreated.strftime("%Y-%m-%dT%H:%M:%S.0000000Z")+'","displayname":"SSH Sensor","location":"Azure DC Singapore","measurename":"SSH Attempt","unitofmeasure":"count","value":1,"ip":"'+ip+'"}'
                        print('sending event at ' +messagetosend)
                        sbs.send_event('ehdevices', messagetosend)
                         
                       else :
                           print('skipping')
                   elif timecreated  > lastRunWaterMark:
                      if isfirstrunRepeat == 1 :
                          #assign to last row executed
                          thisRunWaterMark=timecreated
                          isfirstrunRepeat=0
                      if 'reverse mapping checking getaddrinfo for' in text:
                        count+=1
                        dns= text.split('for ')[1].split(' [')[0]
                        ip= text.split('for ')[1].split(' failed')[0].split('[')[1].split(']')[0]
                        messagetosend = '{"guid":"62X74059-A444-4797-8A7E-526C3EF9D64B","organization":"SG MIC","timecreated":"'+timecreated.strftime("%Y-%m-%dT%H:%M:%S.0000000Z")+'","displayname":"SSH Sensor","location":"Azure DC Singapore","measurename":"SSH Reverse Mapping","unitofmeasure":"count","value":1,"dns":"'+dns+'","ip":"'+ip+'"}'
                        print('sending event at ' +messagetosend)
                        sbs.send_event('ehdevices', messagetosend)

                      elif 'Failed password for root' in text:
                        count+=1
                        ip= text.split('from ')[1].split(' port')[0]
                        port= text.split('port ')[1].split(' ssh')[0]
                        messagetosend = '{"guid":"62X74059-A444-4797-8A7E-526C3EF9D64B","organization":"SG MIC","timecreated":"'+timecreated.strftime("%Y-%m-%dT%H:%M:%S.0000000Z")+'","displayname":"SSH Sensor","location":"Azure DC Singapore","measurename":"SSH Failed Login Attempt","unitofmeasure":"count","value":1,"port":"'+port+'","ip":"'+ip+'","user":"root"}'
                        print('sending event at ' +messagetosend)
                        sbs.send_event('ehdevices', messagetosend)

                      elif 'Failed password for invalid user' in text:
                        count+=1 
                        ip= text.split('from ')[1].split(' port')[0]
                        port= text.split('port ')[1].split(' ssh')[0]
                        user = text.split('user ')[1].split(' from')[0]
                        messagetosend = '{"guid":"62X74059-A444-4797-8A7E-526C3EF9D64B","organization":"SG MIC","timecreated":"'+timecreated.strftime("%Y-%m-%dT%H:%M:%S.0000000Z")+'","displayname":"SSH Sensor","location":"Azure DC Singapore","measurename":"SSH Failed Login Attempt","unitofmeasure":"count","value":1,"port":"'+port+'","ip":"'+ip+'","user":"'+user+'"}'
                        print('sending event at ' +messagetosend)
                        sbs.send_event('ehdevices', messagetosend)
                      elif 'Did not receive identification string' in text:
                        count+=1
                        ip = text.split('from ')[1]
                        messagetosend = '{"guid":"62X74059-A444-4797-8A7E-526C3EF9D64B","organization":"SG MIC","timecreated":"'+timecreated.strftime("%Y-%m-%dT%H:%M:%S.0000000Z")+'","displayname":"SSH Sensor","location":"Azure DC Singapore","measurename":"SSH Attempt","unitofmeasure":"count","value":1,"ip":"'+ip+'"}'
                        print('sending event at ' +messagetosend)
                        sbs.send_event('ehdevices', messagetosend)
                      else :
                           print('skipping')
                   else:
                       break; #exit loop
               except:
                     print "Unexpected error:",sys.exc_info()[0]
        except:
            print "Unexpected error:",sys.exc_info()[0]    


        finally:
            file.close()
            outfile = open("last_time_processed", "w")
            outfile.write(thisRunWaterMark.strftime("%Y-%m-%dT%H:%M:%S"))
            outfile.close()
        if count >= 1 :
            print("Processed "+ str(count) +" items from "+ lastRunWaterMark.strftime("%Y-%m-%dT%H:%M:%S")  + " to " + thisRunWaterMark.strftime("%Y-%m-%dT%H:%M:%S"))
			#print("Sleeping for 5 seconds at " + thisRunWaterMark.strftime("%Y-%m-%dT%H:%M:%S"))
        time.sleep(5)
except IOError, (errno, strerror):
        print "I/O Error(%s) : %s" % (errno, strerror)

def sendToAzure(messagetosend):
    sbs.send_event('ehdevices', messagetosend)

