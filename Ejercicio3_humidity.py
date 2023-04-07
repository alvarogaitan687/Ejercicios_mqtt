#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" 
Created on Thu Apr  6 11:45:41 2023

@author: alvaro
"""
from paho.mqtt.client import Client
import traceback
import sys

K0 = 20
K1 = 30

def on_message(client, userdata, msg):
    print(msg.topic, msg.payload)
    n = float (msg.payload)
    if msg.topic == 'temperature/t1':
        if n > K0 and userdata['humidity'] == False:
            client.subscribe('humidity')
            userdata['humidity'] = True
        elif n < K0 and userdata['humidity'] == True:
            client.unsubscribe('humidity')
            userdata['humidity'] = False
    if msg.topic == 'humidity':
        if n > K1:
            client.unsubscribe('humidity')
            userdata['humidity'] = False

def main(broker):
    userdata = {
        'humidity':False
    }
    client = Client(userdata= userdata)
    client.on_message = on_message

    print(f'Connecting on channels numbers on {broker}')
    client.connect(broker)

    client.subscribe('temperature/t1')

    client.loop_forever()


if __name__ == "__main__":
    import sys
    if len(sys.argv)<2:
        print(f"Usage: {sys.argv[0]} broker")
    broker = sys.argv[1]
    main(broker)
