from kivy import Config
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.togglebutton import ToggleButton

Config.set("graphics", "width", 480)
Config.set("graphics", "height", 320)


class KioskApp(App):
    def build(self):
        price_keypad: GridLayout = self.root.ids.price_keypad

        for char in "7890456.123":
            price_keypad.add_widget(Button(text=char))

        price_keypad.add_widget(Button(text="Backspace"))

        products_keypad: GridLayout = self.root.ids.products_keypad

        for p in range(6):
            products_keypad.add_widget(ToggleButton(text=f"Product {p + 1}"))
