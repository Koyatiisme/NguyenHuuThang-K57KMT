from sense_emu import SenseHat
import time

sense = SenseHat()

try:
    while True:
        temperature = sense.get_temperature()
        humidity = sense.get_humidity()
        joystick_action = "joysticj idle"
        
        for event in sense.stick.get_events():
            if event.action == "pressed":
                joystick_action = f"Joystick {event.direction} pressed"
            elif event.action == 'held':
                joystick_action = f"Joystick {event.direction} held"
            elif event.action == 'released':
                 joystick_action = f"Joystick {event.direction} released"
        
        print(f"Nhiet do: {temperature: .2f}C")
        print(f"Do am: {humidity: .2f}%")
        print(f"trang thai Joystick: {joystick_action}C")
        
        time.sleep(1000)
        
except KeyboardInterrupt:
    print("End")