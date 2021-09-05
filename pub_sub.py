# python 3.6

import random
import time

from paho.mqtt import client as mqtt_client


broker = '3.221.33.231'
port = 1883
topic = "info/0000000000123"

# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 1000)}'
# username = 'emqx'
# password = 'public'

def connect_mqtt():
    now0 = time.time()
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            now1 = time.time()
            now = now1 - now0
            print(f"Connected to MQTT Broker! `{now}` ")
            time.sleep(10)
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
  
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def publish(client):
    msg_count = 0
    while True:
        
        msg = f"messages: {msg_count}"
        result = client.publish(topic, msg)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            
            print(f"Send `{msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")
        msg_count += 1

def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        
        
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic and time `")

    client.subscribe(topic)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_start()
    publish(client)


if __name__ == '__main__':
    run()