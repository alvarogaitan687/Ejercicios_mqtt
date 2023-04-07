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
import random

def on_message(client, userdata, msg):
    print(msg.topic, msg.payload)
    try:
        n =  float(msg.payload)
        if msg.topic == 'temperature/t1':
            if userdata['maximo_t1'] < n:
                userdata['maximo_t1'] = n
            if userdata['minimo_t1'] > n:
                userdata['minimo_t1'] = n
            if userdata['maximo'] < n:
                userdata['maximo'] = n
            if userdata['minimo'] > n:
                userdata['minimo'] = n
            userdata['total_t1'] += n
            userdata['total'] += n
            userdata['numero_datos_t1'] += 1
            userdata['numero_datos'] += 1
        if msg.topic == 'temperature/t2':
            if userdata['maximo_t2'] < n:
                userdata['maximo_t2'] = n
            if userdata['minimo_t2'] > n:
                userdata['minimo_t2'] = n
            if userdata['maximo'] < n:
                userdata['maximo'] = n
            if userdata['minimo'] > n:
                userdata['minimo'] = n
            userdata['total_t2'] += n
            userdata['total'] += n
            userdata['numero_datos_t2'] += 1
            userdata['numero_datos'] += 1
    except ValueError:
        pass
    except Exception as e:
        raise e

def media (suma_total, num):
    return suma_total/num
def main(broker):
    userdata = {
        'maximo_t1': 0,
        'minimo_t1': 10000000,
        'total_t1': 0,
        'numero_datos_t1':0,
        'maximo_t2': 0,
        'minimo_t2': 10000000,
        'total_t2': 0,
        'numero_datos_t2':0,
        'maximo': 0,
        'minimo': 10000000,
        'total': 0,
        'numero_datos':0,
    }
    client = Client(userdata=userdata)
    client.on_message = on_message

    print(f'Connecting on channels numbers on {broker}')
    client.connect(broker)
    
    client.subscribe('temperature/#')

    client.loop_start()
    t0 = time.time()

    while True:
        if (time.time()-t0)>4: #Cuando llegamos a x=4 seg publicamos los resultados hasta la fecha 
            media_t1 = media (userdata['total_t1'], userdata['numero_datos_t1'])
            media_t2 = media (userdata['total_t2'], userdata['numero_datos_t2'])
            mediat = media (userdata['total'], userdata['numero_datos'])
            client.publish('/clients/maximo_t1', f'{userdata["maximo_t1"]}')
            client.publish('/clients/minimo_t1', f'{userdata["minimo_t1"]}')
            client.publish('/clients/media_t1', f'{media_t1}')
            client.publish('/clients/maximo_t2', f'{userdata["maximo_t2"]}')
            client.publish('/clients/minimo_t2', f'{userdata["minimo_t2"]}')
            client.publish('/clients/media_t2', f'{media_t2}')
            client.publish('/clients/maximo', f'{userdata["maximo"]}')
            client.publish('/clients/minimo', f'{userdata["minimo"]}')
            client.publish('/clients/media', f'{mediat}')
            time.sleep(random.random())
            t0 = time.time()
            


if __name__ == "__main__":
    import sys
    if len(sys.argv)<2:
        print(f"Usage: {sys.argv[0]} broker")
    broker = sys.argv[1]
    main(broker)
