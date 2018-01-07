
from time import sleep
import paho.mqtt.client as mqtt
import ssl
import socket
import os
import json
import getpass

username = raw_input("Please type your Username: ");
if(username == 'dczf'):
    password = getpass.getpass("Please type your Password: ");
    if(password == '1234') :
        print('logging in...');
        sleep(2);
        command = raw_input("What command would you like to do?: on/off     ");
        mqtt_client=mqtt.Client(client_id="connRasp",clean_session=True)
        def on_connect(mqttc,obj,flags,rc):
            print("Connection returned result: " + str(rc) )

        def on_message(mqttc,obj,msg):
            json_data = msg.payload
            print("Message received:"+msg.topic+"|Qos: "+str(msg.qos)+" | Data Received:" + str(msg.payload))


        mqtt_client.on_connect=on_connect
        mqtt_client.on_message=on_message

        awshost="a1bnqb5bc7dkjl.iot.us-west-2.amazonaws.com"
        awsport=8883
        caPath="./connRasp/root-CA.pem"
        certPath="./connRasp/connectRasp.cert.pem"
        keyPath="./connRasp/connectRasp.private.key"

        mqtt_client.tls_set(caPath,certfile=certPath,keyfile=keyPath,tls_version=ssl.PROTOCOL_TLSv1_2,ciphers=None)
        mqtt_client.connect(awshost,awsport,keepalive=90)
        print('succeed....')
        mqtt_client.loop_start()
        button = 1

        mqtt_client.subscribe("$aws/things/MyRaspberryPi/shadow/update/accepted",qos=0)
        payload = "{\"state\":{\"desired\":{\"light\":\""+str(command)+"\",\"luminous\":\"###\"}}}"
        print(payload)
        mqtt_client.publish("$aws/things/MyRaspberryPi/shadow/update", payload, 0, True)
    else:
        print('logging in...')
        sleep(3);
        print('sorry, your password is wrong');
else:
    sleep(2);
    print('sorry, your username doesn\'t exist');
