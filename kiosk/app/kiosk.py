import json
import weakref

from kivy import Config
from kivy.app import App
from kivy.network.urlrequest import UrlRequest
from kivy.properties import AliasProperty, DictProperty, NumericProperty, StringProperty
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.modalview import ModalView
from kivy.uix.screenmanager import NoTransition, Screen, ScreenManager
from kivy.uix.togglebutton import ToggleButton

from ..utils import get_product_names

Config.set("graphics", "width", 480)
Config.set("graphics", "height", 320)


def _submit_succeeded(request, result):
    StatusModalView(text="Success").open()


def _submit_failed(request, result):
    StatusModalView(text="Failure").open()


class StatusModalView(ModalView):
    text = StringProperty()
    prev = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        ref = StatusModalView.prev  # no walruses in 3.7
        if ref:
            modal: "StatusModalView" = ref()
            if modal:
                modal.dismiss()

        StatusModalView.prev = weakref.ref(self)


class EditScreen(Screen):
    price = NumericProperty()
    product_ids = DictProperty()  # there's no SetProperty, this is the closest match

    product_count = AliasProperty(lambda self: len(self.product_ids), bind=("product_ids",))

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
        price_keypad: GridLayout = self.ids.price_keypad

        for char in "7890456.123":
            button = Button(text=char)
            button.on_press = lambda char_copy=char: self._add_price_char(char_copy)
            price_keypad.add_widget(button)

        button = Button(text="Backspace")
        button.on_press = lambda: self._delete_price_char()
        price_keypad.add_widget(button)

        products_keypad: GridLayout = self.ids.products_keypad

        for id_, name in enumerate(get_product_names()):
            button = ToggleButton(text=name)
            button.on_press = lambda id_copy=id_, button_copy=button: self._toggle_product_id(id_copy, button_copy)
            products_keypad.add_widget(button)

    def submit(self):
        StatusModalView(text="Please wait...").open()
        UrlRequest(
            "http://localhost:5000",
            method="POST",
            req_body=json.dumps({"price": self.price, "product_ids": list(self.product_ids.keys())}),
            req_headers={"Content-Type": "application/json"},
            on_success=_submit_succeeded,
            on_failure=_submit_failed,
        )


class ListScreen(Screen):
    pass


class KioskApp(App):
    def build(self):
        sm = ScreenManager(transition=NoTransition())
        sm.add_widget(EditScreen(name="edit"))
        sm.add_widget(ListScreen(name="list"))

        sm.get_screen("edit").build()

        return sm
