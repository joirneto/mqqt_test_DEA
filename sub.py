# python3.6

import random
import base64

from paho.mqtt import client as mqtt_client


broker = '3.221.33.231'
port = 1883
topic = "info/12340000000000"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 100)}'
# username = 'emqx'
# password = 'public'

def ecg(mensagem):
    import matplotlib.pyplot
    from numpy.core.fromnumeric import size

    linha = []
    for palavra in mensagem:
        for letra in palavra:
            linha.append(letra)

    s1= linha[32:2532]

    i=0

    w=[]
    while i < size(s1)-1:
        aux = s1[i] + '' + s1[i+1]
        w.append(aux)
        i +=2

    D = []
    for val in w:
        D.append(int(val,16))

    F = 5/size(D)
    aux = F

    G = []
    while F <= 5:
        G.append(F)
        F+= aux
    
    if(size(D)>size(G)):
        del(D[size(D)-1])

    matplotlib.pyplot.plot(G, D)
    matplotlib.pyplot.show()

def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)

    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):

        res = ''.join(format(x, '02x') for x in msg.payload)

        ecg(res)

        print(f"{res}")

    client.subscribe(topic)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run()






