import paho.mqtt.client as mqtt
import json
import random
import time

client = mqtt.Client()
client.connect("test.mosquitto.org", 1883, 60)

while True:
    # Tạo dữ liệu ngẫu nhiên
    temperature = round(random.uniform(25, 35), 2)
    humidity = round(random.uniform(60, 90), 2)

    # Gửi dữ liệu lên MQTT
    client.publish("sensor/temperature", json.dumps({"temperature": temperature}))
    client.publish("sensor/humidity", json.dumps({"humidity": humidity}))

    print(f"Đã gửi: T={temperature}°C, H={humidity}%")
    time.sleep(5)

