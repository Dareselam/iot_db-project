import paho.mqtt.client as mqtt
import json
import time
import random

client = mqtt.Client()
client.connect("localhost", 1883, 60)

while True:
    timestamp = int(time.time())

    # Temperature sensor
    temp_data = {
        "sensor": "temperature",
        "value": round(random.uniform(20, 35), 2),
        "timestamp": timestamp
    }
    client.publish("sensors/temperature", json.dumps(temp_data))

    # Air quality sensor
    air_data = {
        "sensor": "air_quality",
        "pm25": round(random.uniform(10, 60), 1),
        "pm10": round(random.uniform(20, 80), 1),
        "aqi": random.randint(50, 150),
        "timestamp": timestamp
    }
    client.publish("sensors/air_quality", json.dumps(air_data))

    # Network sensor
    network_data = {
        "sensor": "network",
        "device_id": f"device_{random.randint(1, 5)}",
        "connected_to": f"gateway_{random.randint(1, 2)}",
        "timestamp": timestamp
    }
    client.publish("sensors/network", json.dumps(network_data))

    print("Published all sensor data")
    time.sleep(5)
