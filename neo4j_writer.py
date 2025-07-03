import paho.mqtt.client as mqtt
from py2neo import Graph, Node, Relationship
import json
import time

# Neo4j connection
graph = Graph("bolt://localhost:7687", auth=("neo4j", "password"))

# MQTT callbacks
def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker with result code " + str(rc))
    client.subscribe("sensors/network")
    
def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())
        device_id = data["device_id"]
        gateway_id = data["connected_to"]

        start = time.time()  # Start timing

        # Create or merge nodes
        device = Node("Device", name=device_id)
        gateway = Node("Gateway", name=gateway_id)
        graph.merge(device, "Device", "name")
        graph.merge(gateway, "Gateway", "name")

        # Create or merge relationship
        connected = Relationship(device, "CONNECTED_TO", gateway)
        graph.merge(connected)

        end = time.time()  # End timing

        print(f"Stored relationship: {device_id} → {gateway_id}")
        print(f"DB Insert took {end - start:.4f} seconds")

    except Exception as e:
        print("Neo4j Error:", e)

# MQTT client setup
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)
client.loop_forever()
