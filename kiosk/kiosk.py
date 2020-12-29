from kivy import Config
from kivy.app import App
from kivy.properties import NumericProperty
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.togglebutton import ToggleButton

Config.set("graphics", "width", 480)
Config.set("graphics", "height", 320)


class KioskApp(App):
    price = NumericProperty()

    def _add_price_char(self, char: str):
        try:
            self.price = int(f"{self.price}{char}")
        except ValueError:
            return

    def _delete_price_char(self):
        try:
            self.price = int(f"0{self.price}"[:-1])
        except ValueError:
            return

    def build(self):
        price_keypad: GridLayout = self.root.ids.price_keypad

        for char in "7890456.123":
            button = Button(text=char)
            button.on_press = lambda char_copy=char: self._add_price_char(char_copy)
            price_keypad.add_widget(button)

        button = Button(text="Backspace")
        button.on_press = lambda: self._delete_price_char()
        price_keypad.add_widget(button)

        products_keypad: GridLayout = self.root.ids.products_keypad

        for p in range(6):
            products_keypad.add_widget(ToggleButton(text=f"Product {p + 1}"))
