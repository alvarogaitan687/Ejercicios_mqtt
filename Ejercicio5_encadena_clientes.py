"""
Created on Thu Apr  6 11:45:41 2023

@author: alvaro
"""
from paho.mqtt.client import Client
import traceback
import sys
import time 

def on_message(client, userdata, msg):
    print(msg.topic, msg.payload)
    n =  float(msg.payload)
    if n%1 == 0: #Si llega un numero entero 
        print('hola on_message')
        userdata['client_3'].subscribe(userdata['client_2']._userdata['topic_s']) #Donde client_2 va a publicar un mensaje cuando se detenga (su temporizador) y será el que paute a client_3 que debe publicar la media que lleva hasta la fecha 
        userdata['client_3'].subscribe('humidity') 
        userdata['client_3'].loop_start()
        userdata['client_2'].loop_start()
        time.sleep(float(userdata['client_2']._userdata['tiempo_espera']))
        client.publish(userdata['client_2']._userdata['topic_s'], userdata['client_2']._userdata['mensaje'])

def on_message1(client, userdata, msg):
    if msg.payload == b'RING RING':
        client.unsubscribe('humidity')
        client.publish('/clients/alvaro', media(userdata['suma_total'], userdata['num_datos']))

    if msg.topic == 'humidity':
        n =  float(msg.payload)
        userdata['suma_total'] += n
        userdata['num_datos'] += 1
        
            
            
def media (suma_total, num_total):
    return suma_total/num_total

"""Client_1 se subscribe a numbers cuando llega un entero activa un temporizador en client_2 y a su vez
comienza a leer en 'humidity' mediante el client_3 acumulando la suma total de los numeros que va leyendo 
asi como el numero de ellos para acabar publicando la media en /clients/alvaro cuando el temporizador de client_2 se detiene"""
def main(broker):
    userdata2 = {
        'tiempo_espera':'10', 
        'topic_s': '/clients/alvaro',
        'mensaje': 'RING RING'
    }
    userdata3 = {
        'suma_total':0,
        'num_datos':0
    }
    client_2 = Client(userdata = userdata2)
    client_3 = Client(userdata = userdata3)
    client_1 = Client(userdata = {'client_2':client_2,'client_3':client_3}) 
    client_1.on_message = on_message 
    client_3.on_message = on_message1
    print(f'Connecting on channels numbers on {broker}')
    client_1.connect(broker)
    client_2.connect(broker)
    client_3.connect(broker)
    client_1.subscribe('numbers')
    client_1.loop_forever()
    client_2.loop_forever()
    client_3.loop_forever()

if __name__ == "__main__":
    import sys
    if len(sys.argv)<2:
        print(f"Usage: {sys.argv[0]} broker")
    broker = sys.argv[1]
    main(broker)
    
