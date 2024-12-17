from flask import Flask, render_template
import time
import threading

app = Flask(__name__)

# Hàm giả lập đọc nhiệt độ từ cảm biến
def get_temperature():
  # Thay thế đoạn này bằng code đọc nhiệt độ thực tế từ cảm biến trên Raspberry Pi
  # Ví dụ: sử dụng thư viện sense_hat
  from sense_emu import SenseHat
  sense = SenseHat()
  temp = sense.get_temperature()
  return temp

def save_temperature_to_db(temperature):
    conn = sqlite3.connect('temperature_data.db')  # Kết nối hoặc tạo database
    cursor = conn.cursor()

    # Tạo bảng nếu chưa tồn tại
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS temperatures (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            temperature REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Lưu nhiệt độ vào database
    cursor.execute("INSERT INTO temperatures (temperature) VALUES (?)", (temperature,))
    conn.commit()
    conn.close()
import numpy as np

def moving_average(past_values, t, n=5):
  """
  Applies a moving average filter to the temperature data.

  Args:
    past_values: A list or numpy array of past temperature values.
    t: The current temperature value.
    n: The number of past samples to consider (window size).

  Returns:
    The filtered temperature value.
  """
  if len(past_values) < n:
    return np.mean(past_values + [t]) # Use all available data if less than n samples

  return np.mean(past_values[-n:] + [t])

past_temp = []

import pyrebase

# Firebase configuration (replace with your own)
firebaseConfig = {
  "apiKey": "AIzaSyBT6hsnuEz43H_Yzd611VZYR2IsXX0-tu0",
  "authDomain": "huuthang-21t01.firebaseapp.com",
  "databaseURL": "https://huuthang-21t01-default-rtdb.firebaseio.com",
  "projectId": "huuthang-21t01",
  "storageBucket": "huuthang-21t01.firebasestorage.app",
  "messagingSenderId": "842173351798",
  "appId": "1:842173351798:web:7356bff3715ed5d5629c57",
}

firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()

def save_temperature_to_firebase(temperature):
    import datetime
    now = datetime.datetime.now()
    date_time = now.strftime("%Y-%m-%d %H:%M:%S")
    data = {
        "ngay_thang": now.strftime("%Y-%m-%d"),
        "thoi_gian": now.strftime("%H:%M:%S"),
        "nhiet_do": temperature
    }
    db.child("Nhiet_Do").push(data) # Push data to Firebase
def push_optimized_data():
    global previous_T, current_data  # Sử dụng biến toàn cục
    while True:
        try:
            # Đọc nhiệt độ, độ ẩm và áp suất từ SenseHAT
            current_temp = round(sense.get_temperature(), 2)
            humidity = round(sense.get_humidity(), 2)
            pressure = round(sense.get_pressure(), 2)

            # Lấy trạng thái joystick
            joystick_events = sense.stick.get_events()
            joystick_state = "Không có sự kiện"
            if joystick_events:
                last_event = joystick_events[-1]
                joystick_state = f"{last_event.direction} - {last_event.action}"

            # So sánh sự thay đổi nhiệt độ với ngưỡng
            if abs(current_temp - previous_T) > temperature_change_threshold:
                # Tính T_cập_nhật
                T_cap_nhat = round((current_temp + previous_T) / 2, 2)
                # Gửi dữ liệu lên Firebase
                sensor_data = {
                    "temperature": T_cap_nhat,
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
                }
                database.child("OptimizedSensorData").set(sensor_data)
                print("Đã gửi dữ liệu lên Firebase:", sensor_data)

                previous_T = T_cap_nhat  # Cập nhật T

            # Cập nhật dữ liệu hiển thị trên web
            current_data["t_hien_tai"] = current_temp
            current_data["T_cap_nhat"] = T_cap_nhat
            current_data["humidity"] = humidity
            current_data["joystick_state"] = joystick_state
            current_data["pressure"] = pressure

            # Tạm dừng 5 giây
            time.sleep(5)

        except Exception as e:
            print("Lỗi xảy ra:", e)

@app.route("/")
def index():
    global past_temp
    temp = get_temperature()
    avg = moving_average(past_temp, temp)
    past_temp.append(avg)
    return render_template("index.html", temperature=temp, avg_temperature=avg)

if __name__ == "__main__":
    threading.Thread(target=save_temperature_to_firebase).start()
    app.run(host='0.0.0.0', port=5000, debug=True)