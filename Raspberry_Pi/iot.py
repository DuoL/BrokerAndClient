import RPi.GPIO as gpio
import time
import paho.mqtt.client as mqtt
import ssl
import socket
import os
import json,time
import sys
import codecs

mqtt_client=mqtt.Client(client_id="MyRaspberryPi",clean_session=True)
gpio.setmode(gpio.BOARD)
gpio.setup(22,gpio.OUT)
DEBUG = 1
HI = 13
gpio.setmode(gpio.BOARD)
gpio.setup(HI,gpio.OUT)
def RCtime(RCpin):
    reading=0
    gpio.setup(RCpin,gpio.OUT)
    gpio.output(RCpin,gpio.LOW)
    time.sleep(0.5)
    gpio.setup(RCpin,gpio.IN)
    while(gpio.input(RCpin)==gpio.LOW):
        reading+=1
    return reading

def photo(reading):
    out=""
    if reading<=3000:
        out="O:"
        ledOut(0)
        return out
    out=""
    ledOut(1)
    return out

def ledOut(state):
    if state==0:
        gpio.output(HI,False)
        return 0
    if state==1:
        gpio.output(HI,True)
        return 0
    return 1

liangdu = 0

def on_connect(mqttc,obj,flags,rc):
    print("Connection returned result: " + str(rc) )

def on_message(mqttc,obj,msg):
    payloadJson =json.loads(msg.payload.decode())
    switch = payloadJson["state"]["desired"]["light"]
    print(switch)
    lightlevel = payloadJson["state"]["desired"]["luminous"]
    x = 1
    if(switch=="on" or x != 0):
        sys.stdout.write(photo(RCtime(11)))
        sys.stdout.flush()
        liangdu = RCtime(11)
        payload="{\"state\":{\"desired\":{\"light\":\"on\",\"luminous\":"+str(RCtime(11))+"}}}"
        time.sleep(1);

        mqtt_client.publish("$aws/things/MyRaspberryPi/shadow/update",payload, qos=1)

    if(switch=="off"):
        payload = "{\"state\":{\"desired\":{\"light\":\"off\",\"luminous\":\"-1\"}}}"
        mqtt_client.publish("$aws/things/MyRaspberryPi/shadow/update",payload, qos=1)
        exit()

def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed: "+str(mid)+" "+str(granted_qos))

mqtt_client.on_connect=on_connect
mqtt_client.on_subscribe=on_subscribe
mqtt_client.on_message=on_message


awshost="a1bnqb5bc7dkjl.iot.us-west-2.amazonaws.com"
awsport=8883
caPath="./certs/root-CA.crt"
certPath="./certs/d706eb9452-certificate.pem.crt"
keyPath="./certs/d706eb9452-private.pem.key"

mqtt_client.tls_set(caPath,certfile=certPath,keyfile=keyPath,tls_version=ssl.PROTOCOL_TLSv1_2,ciphers=None)
mqtt_client.connect(awshost,awsport)
print('succeed....')
#mqtt_client.subscribe("$aws/things/MyRaspberryPi", qos=0)                                                                              
mqtt_client.subscribe("$aws/things/MyRaspberryPi/shadow/update/accepted", qos=0)
#payload="{\"state\":{\"desired\":{\"light\":"+str(liangdu)+"}}}"                                                                       
#mqtt_client.publish("$aws/things/MyRaspberryPi/shadow/update",payload, qos=1)                                                          
mqtt_client.loop_forever()
