import json
import paho.mqtt.client as mqtt
import os
from dotenv import load_dotenv
import requests


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("events/chile")
    client.subscribe("events/requests")
    client.subscribe("events/validation")
    client.subscribe("events/auctions")


def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))

    if (msg.topic == "events/chile"):
        requests.post(
            "http://api:8000/events/",
            headers={"Content-type": "application/json"},
            json=json.loads(msg.payload)
        )
    elif (msg.topic == "events/requests"):
        requests.post(
            "http://api:8000/requests/",
            headers={"Content-type": "application/json"},
            json=json.loads(msg.payload)
        )
    elif (msg.topic == "events/validation"):
        requests.post(
            "http://api:8000/validations/",
            headers={"Content-type": "application/json"},
            json=json.loads(msg.payload)
        )
    elif (msg.topic == "events/auctions"):
        requests.post(
            "http://api:8000/auctions/",
            headers={"Content-type": "application/json"},
            json=json.loads(msg.payload)
        )


load_dotenv()

MY_ENV_VAR = os.getenv('MY_ENV_VAR')

host = os.getenv('HOST')
port = os.getenv('PORT')
user = os.getenv('USER_MQTT')
password = os.getenv('PASSWORD')

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.username_pw_set(user, password=password)
client.connect(host, int(port))

client.loop_forever()
