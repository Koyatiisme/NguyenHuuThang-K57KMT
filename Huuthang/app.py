from flask import Flask, render_template
from sense_emu import SenseHat

app = Flask(__name__)
sense = SenseHat()

@app.route('/')
def home():
    temperature = sense.get_temperature()
    humidity = sense.get_humidity()
    joystick_status = "Khong co su kien"
    
    for event in sense.stick.get_events():
        if event.action == "pressed":
            joystick_status = f"Joystick {event.direction} pressed"
        elif event.action == 'held':
            joystick_status = f"Joystick {event.direction} held"
        elif event.action == 'released':
            joystick_status = f"Joystick {event.direction} released"
    return render_template("index.html",
                           temperature=temperature,
                           humidity=humidity,
                           joystick_status=joystick_status)

if __name__=="__main__":
    app.run(host="0.0.0.0", port=5000)
