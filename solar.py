#!/usr/bin/python

#Settings

sideid = "" #monitoring.solaredge.com siteID
serial = "" #monitoring.solaredge.com Serial inverter
apikey = "" #monitoring.solaredge.com API key
idx_temp = "" #idx of the temperature sensor
idx_watt = "" #idx of the meter"
idx_acvoltage = "" #idx of the acVoltage meter
idx_dcvoltage = "" #idx of the dcVoltage meter

# Settings for the domoticz server
domoticzserver=""

import urllib
#import urllib.request
import sys
from datetime import datetime, timedelta
from xml.dom import minidom
import urllib2

#print (sys.version) 

now = datetime.now()
minusfive = now - timedelta(minutes=now.minute % 5 + 15,
				seconds=now.second,
				microseconds=now.microsecond)
timenow = now - timedelta(seconds=now.second,
                                microseconds=now.microsecond)

#print minusfive
#print timenow

download = "https://monitoringapi.solaredge.com/equipment/"+sideid+"/"+serial+"/data.xml?startTime="+str(minusfive)+"&endTime="+str(timenow)+"&api_key="+apikey

print download

urllib.urlretrieve (download, "/home/pi/domoticz/scripts/data.xml")

doc = minidom.parse("/home/pi/domoticz/scripts/data.xml")

count_xml = doc.getElementsByTagName("count")[0]
count_reading = count_xml.firstChild.data

print count_reading

if count_reading == "0" :
	print "nul"
	temp = "0"
        watt = "0"
        total = "0"
        acVoltage = "0"
        dcVoltage = "0"

else:
	print "not null"
	temp_xml = doc.getElementsByTagName("temperature")[0]
        temp = temp_xml.firstChild.data
        watt_xml = doc.getElementsByTagName("activePower")[0]
        watt = watt_xml.firstChild.data
        total_xml = doc.getElementsByTagName("totalEnergy")[0]
        total = total_xml.firstChild.data
        acVoltage_xml = doc.getElementsByTagName("acVoltage")[0]
        acVoltage = acVoltage_xml.firstChild.data
        dcVoltage_xml = doc.getElementsByTagName("dcVoltage")[0]
        dcVoltage = dcVoltage_xml.firstChild.data

print temp
print watt
print total 
print acVoltage
print dcVoltage

domoticzurl1 = "http://"+domoticzserver+"/json.htm?type=command&param=udevice&idx="+idx_temp+"&svalue="+temp
domoticzurl2 = "http://"+domoticzserver+"/json.htm?type=command&param=udevice&idx="+idx_watt+"&svalue="+watt+";"+total
domoticzurl3 = "http://"+domoticzserver+"/json.htm?type=command&param=udevice&idx="+idx_acvoltage+"&svalue="+acVoltage
domoticzurl4 = "http://"+domoticzserver+"/json.htm?type=command&param=udevice&idx="+idx_dcvoltage+"&svalue="+dcVoltage

print domoticzurl1
print domoticzurl2
print domoticzurl3
print domoticzurl4

#urllib2.Request(domoticzurl1)
urllib.urlretrieve (domoticzurl1, "/home/pi/domoticz/scripts/solar_temp.log")
urllib.urlretrieve (domoticzurl2, "/home/pi/domoticz/scripts/solar_watt.log")
urllib.urlretrieve (domoticzurl3, "/home/pi/domoticz/scripts/solar_acVoltage.log")
urllib.urlretrieve (domoticzurl4, "/home/pi/domoticz/scripts/solar_dcVoltage.log")
