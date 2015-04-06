import ephem
import requests
import ntplib
import math
import os
from datetime import datetime
import time
import Adafruit_BBIO.GPIO as GPIO
GPIO.cleanup()
GPIO.setup("P8_8", GPIO.OUT)
GPIO.setup("P8_12", GPIO.OUT)
GPIO.setup("P8_18", GPIO.OUT)



GPIO.output("P8_8", GPIO.LOW)
GPIO.output("P8_12", GPIO.LOW)
GPIO.output("P8_18", GPIO.LOW)


os.system("date -s \"$(curl -sD - google.com | grep ^Date: | cut -d' ' -f3-6)Z\" ")

city = ephem.Observer()
city.lat = '39.9'
city.lon = '116.38'

while (1):
	r =  requests.get('http://www.celestrak.com/NORAD/elements/stations.txt')


	r =  str(r.text).split('\n')


	print r[0]
	print r[1]
	print r[2]


	city.date = datetime.utcnow()

	sun = ephem.Sun(city)

	iss = ephem.readtle(r[0],r[1],r[2])

	iss.compute(datetime.utcnow())

	chn = ephem.readtle(r[3],r[4],r[5])

        chn.compute(datetime.utcnow())


	print "Current ISS Lat Long is:"
	print iss.sublat, iss.sublong

 	print "Current CHN Lat Long is:"
        print chn.sublat, chn.sublong


	if math.fabs(math.degrees(city.lat-iss.sublat)) < 3 and math.fabs(math.degrees(city.long-iss.sublong)) < 3 :
		print "YOU ARE UNDER ISS OBSERVATION"
		print (iss.sublong), (iss.sublat)
		GPIO.output("P8_8", GPIO.HIGH)

	else:
		print "YOU ARE NOT UNDER ISS OBSERVATION"
                print (iss.sublong), (iss.sublat) 
		GPIO.output("P8_8", GPIO.LOW)

	
        if math.fabs(math.degrees(city.lat-chn.sublat)) < 3 and math.fabs(math.degrees(city.long-chn.sublong)) < 3 :
                print "YOU ARE UNDER CHN OBSERVATION"
                print (chn.sublong), (chn.sublat)
		GPIO.output("P8_12", GPIO.HIGH)


        else:
             	print "YOU ARE NOT UNDER CHN OBSERVATION"
                print (chn.sublong), (chn.sublat)
		GPIO.output("P8_12", GPIO.LOW)

