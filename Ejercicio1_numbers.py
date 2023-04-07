#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  6 11:45:41 2023

@author: alvaro
"""
from paho.mqtt.client import Client
import traceback
import sys


def on_message(client, userdata, msg):
    print(msg.topic, msg.payload)
    try:
        n =  float(msg.payload)
        if n%1 == 0:
            userdata['frec_enteros'] += 1
            client.publish('/clients/frec_enteros', f'{userdata["frec_enteros"]}')
            client.publish('/clients/enteros', n)
        else:
            userdata['frec_reales'] += 1
            client.publish('/clients/frec_reales', f'{userdata["frec_reales"]}')
            client.publish('/clients/reales', n)
    except ValueError:
        pass
    except Exception as e:
        raise e


def main(broker):
    userdata = {
        'frec_enteros': 0,
        'frec_reales':0
    }
    client = Client(userdata=userdata)
    client.on_message = on_message
    print(f'Connecting on channels numbers on {broker}')
    client.connect(broker)
    
    client.subscribe('numbers')
    client.loop_forever()


if __name__ == "__main__":
    import sys
    if len(sys.argv)<2:
        print(f"Usage: {sys.argv[0]} broker")
    broker = sys.argv[1]
    main(broker)
