import tkinter as tk
from tkinter import scrolledtext, messagebox
import paho.mqtt.client as mqtt
import json
import sqlite3
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time
import threading

#Kết nối CSDL SQLite
conn = sqlite3.connect("sensor_data.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS SensorData (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    temperature REAL,
    humidity REAL
)
""")
conn.commit()

#App Tkinter
root = tk.Tk()
root.title("Ứng dụng giám sát dữ liệu cảm biến (MQTT)")
root.geometry("800x600")

# Hiển thị log
log_area = scrolledtext.ScrolledText(root, width=80, height=10)
log_area.pack(pady=5)

# Khung chứa biểu đồ
fig, ax = plt.subplots(figsize=(6,3))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()

# Dữ liệu để vẽ biểu đồ
time_data = []
temp_data = []
humid_data = []

# Hàm cập nhật biểu đồ
def update_chart():
    ax.clear()
    ax.plot(time_data, temp_data, label="Temperature (°C)", color="red")
    ax.plot(time_data, humid_data, label="Humidity (%)", color="blue")
    ax.set_xlabel("Time")
    ax.set_ylabel("Value")
    ax.legend()
    ax.grid(True)
    canvas.draw()

#MQTT Callback
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        log_area.insert(tk.END, "✅ Kết nối MQTT thành công\n")
        client.subscribe("sensor/temperature")
        client.subscribe("sensor/humidity")
    else:
        log_area.insert(tk.END, "❌ Kết nối MQTT thất bại\n")

def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())
        log_text = f"[MQTT] {msg.topic} → {data}\n"
        log_area.insert(tk.END, log_text)
        log_area.see(tk.END)

        # Lấy timestamp
        current_time = time.strftime("%H:%M:%S")

        # Lưu vào DB và cập nhật dữ liệu vẽ
        if "temperature" in data:
            cursor.execute("INSERT INTO SensorData(timestamp, temperature, humidity) VALUES (?, ?, ?)", 
                           (current_time, data["temperature"], None))
            temp_data.append(data["temperature"])
            time_data.append(current_time)

        if "humidity" in data:
            cursor.execute("INSERT INTO SensorData(timestamp, temperature, humidity) VALUES (?, ?, ?)", 
                           (current_time, None, data["humidity"]))
            humid_data.append(data["humidity"])
            if current_time not in time_data:
                time_data.append(current_time)

        conn.commit()
        update_chart()

    except Exception as e:
        log_area.insert(tk.END, f"Lỗi xử lý dữ liệu: {e}\n")

#MQTT Client 
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

def start_mqtt():
    try:
        client.connect("test.mosquitto.org", 1883, 60)
        client.loop_forever()
    except Exception as e:
        messagebox.showerror("MQTT Error", str(e))

# Chạy MQTT trong luồng riêng
threading.Thread(target=start_mqtt, daemon=True).start()

root.mainloop()
