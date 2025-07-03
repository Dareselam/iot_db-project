import paho.mqtt.client as mqtt
import json
import time

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("sensors/temperature")

def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())
        temperature = data.get("value")
        timestamp = data.get("timestamp")
        readable_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp))
        print(f"Temperature: {temperature} °C at {readable_time}")
    except Exception as e:
        print("Failed to parse message:", e)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)
client.loop_forever()

