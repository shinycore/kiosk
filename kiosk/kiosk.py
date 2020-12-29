from kivy import Config
from kivy.app import App
from kivy.uix.label import Label

Config.set("graphics", "width", 480)
Config.set("graphics", "height", 320)


class KioskApp(App):
    def build(self):
        return Label(text="Hi")
