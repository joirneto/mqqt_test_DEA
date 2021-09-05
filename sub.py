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

    #Manipulação de uma string para um array de caracteres
    arrayCaracteres = []
    for palavra in mensagem:
        for letra in palavra:
            arrayCaracteres.append(letra)

    #Retirar o cabeçalho
    payloadCaracteres= arrayCaracteres[32:2532]

    #Manipular para um array de pares de caracteres
    i=0
    payloadParesHexa=[]
    while i < size(payloadCaracteres)-1:
        aux = payloadCaracteres[i] + '' + payloadCaracteres[i+1]
        payloadParesHexa.append(aux)
        i +=2

    #Converter de Hexa para int - Valores de 0 a 255
    payloadInt = []
    for val in payloadParesHexa:
        payloadInt.append(int(val,16))

    # Gerando unidade de tempo
    tempo = 5/size(payloadInt)
    
    #Gerando array com todas os valores de tempo
    aux = tempo
    arrayTempo = []
    while tempo <= 5:
        arrayTempo.append(tempo)
        tempo+= aux
    
    #Verificação de dimensões entre dados a serem plotados
    if(size(payloadInt)>size(arrayTempo)):
        del(payloadInt[size(payloadInt)-1])

    #Plotando os dados
    matplotlib.pyplot.plot(arrayTempo, payloadInt)
    matplotlib.pyplot.xlabel('time in seconds')
    matplotlib.pyplot.ylabel('Amplitude (normalised)')
    matplotlib.pyplot.title('Heart beat signal Template')
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
        print(f"Received `{msg.payload}` from `{msg.topic}` topic and time `")
        res = ''.join(format(x, '02x') for x in msg.payload)
        print(f"Received `{res}` from `{msg.topic}` topic and time `")
        ecg(res)

    client.subscribe(topic)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run()






