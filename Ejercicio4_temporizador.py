#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  6 11:45:41 2023

@author: alvaro
"""
from paho.mqtt.client import Client
import traceback
import sys
import time

def main(broker, tiempo_espera, topic_s, mensaje):
    userdata = {
                'tiempo_espera':tiempo_espera, 
                'topic_s':topic_s,
                'mensaje': mensaje
    }
    client = Client(userdata=userdata)
    print(f'Connecting on channels numbers on {broker}')
    client.connect(broker)
    time.sleep(float(userdata['tiempo_espera']))
    client.publish(userdata['topic_s'], userdata['mensaje'])


if __name__ == "__main__":
    import sys
    if len(sys.argv)<4:
        print(f"Usage: {sys.argv[0]} broker topic_s topic_p")
        sys.exit(1)
    broker = sys.argv[1]
    tiempo_espera = sys.argv[2]
    topic_s = sys.argv[3]
    mensaje = sys.argv[4]
    main(broker, tiempo_espera, topic_s, mensaje)