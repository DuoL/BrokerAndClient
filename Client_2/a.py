import paho.mqtt.client as mqtt
import ssl
import socket
import os
import json
import getpass
from time import sleep

username = input("Please type your Username: ");
if(username == 'dczf'):
    password = getpass.getpass("Please type your Password: ");
    if(password == '1234') :
        print('logging in...');
        sleep(2);
        command = input("What command would you like to do?: on/off     ");
        mqtt_client=mqtt.Client(client_id="belz",clean_session=True)
        def on_connect(mqttc,obj,flags,rc):
            if rc == 0:
                print("Connection returned result: " + str(rc) )
                print (1)
                
        def on_message(mqttc,obj,msg):
            print("Message received:"+msg.topic+"|Qos: "+str(msg.qos)+" | Data Received: "+str(msg.payload)) 

        mqtt_client.on_connect=on_connect
        mqtt_client.on_message=on_message

        awshost="a1bnqb5bc7dkjl.iot.us-west-2.amazonaws.com"
        awsport=8883
        caPath="/Users/Belzhang/Desktop/mqtt/root-CA.crt"
        certPath="/Users/Belzhang/Desktop/mqtt/belz.cert.pem"
        keyPath="/Users/Belzhang/Desktop/mqtt/belz.private.key"
        mqtt_client.tls_set(ca_certs=caPath,certfile=certPath,keyfile=keyPath,tls_version=ssl.PROTOCOL_TLSv1_2,ciphers=None)
        mqtt_client.connect(awshost,awsport,keepalive=90)
#payload = "{\"state\":{\"desired\":{\"switch\":\"on\"}},{\"reported\":{\"light\":\"0\"}}}"
#payload = "{\"state\":{\"switch\":\"on\",\"light\":\"0\"}}"
        #payload = "{\"state\":{\"desired\":{\"light\":\"off\",\"luminous\":\"0\"}}}"  
#payload = "{\"state\":{\"switch\":\"on\"}}"
        payload = "{\"state\":{\"desired\":{\"light\":\""+str(command)+"\",\"luminous\":\"###\"}}}"
        mqtt_client.publish("$aws/things/MyRaspberryPi/shadow/update", payload, 0, True)
        mqtt_client.loop_start()
#mqtt_client.subscribe("$aws/things/MyRaspberryPi/shadow/update", qos=0)
    else:
        print('logging in...')
        sleep(3);
        print('sorry, your password is wrong');
else:
    sleep(2);
    print('sorry, your username doesn\'t exist');


