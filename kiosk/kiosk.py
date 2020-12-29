from kivy import Config
from kivy.app import App
from kivy.properties import DictProperty, NumericProperty
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.togglebutton import ToggleButton

Config.set("graphics", "width", 480)
Config.set("graphics", "height", 320)


class KioskApp(App):
    price = NumericProperty()
    product_ids = DictProperty()  # there's no SetProperty, this is the closest match

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

    def _toggle_product_id(self, id_: int, button: ToggleButton):
        if button.state == "normal":
            try:
                del self.product_ids[id_]
            except KeyError:
                pass
        elif button.state == "down":
            self.product_ids[id_] = None

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

        for id_ in range(6):
            button = ToggleButton(text=f"Product {id_ + 1}")
            button.on_press = lambda id_copy=id_, button_copy=button: self._toggle_product_id(id_copy, button_copy)
            products_keypad.add_widget(button)
