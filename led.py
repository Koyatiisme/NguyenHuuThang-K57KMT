from sense_emu import SenseHat

sense = SenseHat()

name = "Huu Thang"

text_color = (0, 255, 0)
back_color = (0, 0, 0)

sense.show_message(name, text_colour = text_color, back_colour=back_color, scroll_speed=2)

sense.clear()