import paho.mqtt.client as mqtt
import json
import time
from pymongo import MongoClient

# MongoDB setup
mongo_client = MongoClient("mongodb://localhost:27017/")
db = mongo_client["iot_project"]
collection = db["temperature_readings"]

# MQTT callbacks
def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT with result code " + str(rc))
    client.subscribe("sensors/air_quality")
    print("Subscribed to topic: sensors/air_quality")



def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())
        start = time.time()
        data["received_at"] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    
        collection.insert_one(data)
        end = time.time()
        print(f"Saved to MongoDB: {data}")
        print(f"DB Insert took {end - start:.4f} seconds")

    except Exception as e:
        print("Error processing message:", e)


# MQTT setup
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)
client.loop_forever()
