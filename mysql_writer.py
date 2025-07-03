import paho.mqtt.client as mqtt
import mysql.connector
import json
import time

# Connect to MySQL (change credentials as needed)
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",  # Default XAMPP MySQL password is empty
    database="iot_data"
)
cursor = conn.cursor()

# MQTT callbacks
def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker with result code " + str(rc))
    client.subscribe("sensors/temperature")





def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())
        sensor = data["sensor"]
        value = data["value"]
        timestamp = data["timestamp"]
        received_at = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

        start = time.time()

        # Insert into MySQL
        cursor.execute("""
            INSERT INTO temperature_readings (sensor, value, timestamp, received_at)
            VALUES (%s, %s, %s, %s)
        """, (sensor, value, timestamp, received_at))
        conn.commit()
        end = time.time()

        print(f"Saved to MySQL: {data}")
        print(f"DB Insert took {end - start:.4f} seconds")

    except Exception as e:
        print("Error:", e)



# MQTT Client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)
client.loop_forever()
