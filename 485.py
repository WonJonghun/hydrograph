#!/urs/bin/env python

import paho.mqtt.client as mqtt
import json
import serial
import re
from datetime import datetime

waterLevelID = 'WID1'
hostIp = '192.168.0.24'


def on_connect(client, userdata, flags, rc):

    if rc == 0:
        print("completely connected")
    else:
        print("Bad connection Returned code=", rc)


def on_disconnect(client, userdata, flags, rc=0):
    print(str(rc))

client = mqtt.Client()
client.on_connect = on_connect
client.on_disconnect = on_disconnect

#ttyS3는 USB포트번호
ser = serial.Serial('/dev/ttyS3', 9600)
ser.flushInput()

client.connect(hostIp, 1883)
client.loop_start()

while 1:
	if ser.inWaiting()>0 :
		val = ser.readline(10)
		hex = val[3:7]
		cm = int(hex,16)
		print(cm,'cm')
		time = datetime.now()
		wl = waterLevelID+'	'+str(cm)+'cm'+'	' + str(time)
		client.publish('test/hello', wl, 1)


client.loop_stop()

client.disconnect()
