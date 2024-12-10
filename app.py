import streamlit as st
from sense_emu import SenseHat
import time

sense = SenseHat()

st.title("WEB HIEN THI NHIET DO VA DO AM")

placeholder = st.empty()

def read_sense_data():
    temperature = sense.get_temperature()
    humidity = sense.get_humidity()
    joystick_action = "Khong co su kien"
    
    for event in sense.stick.get_events():
        if event.action == "pressed":
            joystick_action = f"Joystick {event.direction} pressed"
        elif event.action == 'held':
            joystick_action = f"Joystick {event.direction} held"
        elif event.action == 'released':
            joystick_action = f"Joystick {event.direction} released"
    return temperature, humidity, joystick_action


while True:
    temperature, humidity, joystick_action = read_sense_data()
    with placeholder.container():
        st.write(f"**Nhiet do: ** {temperature:.2f}*C")
        st.write(f"**Do am: ** {humidity:.2f}%")
        st.write(f"**Trang thai Joystick: ** {joystick_action}")
    time.sleep(10)
        
        
        
