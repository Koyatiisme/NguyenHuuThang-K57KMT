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