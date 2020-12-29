from kivy.app import App
from kivy.uix.label import Label


class KioskApp(App):
    def build(self):
        return Label(text="Hi")
