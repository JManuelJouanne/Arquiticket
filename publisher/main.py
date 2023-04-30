import paho.mqtt.client as mqtt
import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request
import _thread

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("events/requests")


@app.post("/requests_create/")
async def send_validation(request: Request):
    info = await request.json()
    client.publish("events/requests", info)


load_dotenv()

MY_ENV_VAR = os.getenv('MY_ENV_VAR')

host = os.getenv('HOST')
port = os.getenv('PORT')
user = os.getenv('USER_MQTT')
password = os.getenv('PASSWORD')

client = mqtt.Client()
client.on_connect = on_connect

client.username_pw_set(user, password=password)
client.connect(host, int(port))

_thread.start_new_thread(client.loop_forever, ())
