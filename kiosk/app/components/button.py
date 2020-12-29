from kivy.properties import StringProperty
from kivy.uix.behaviors import ButtonBehavior, ToggleButtonBehavior
from kivy.uix.boxlayout import BoxLayout


class KBaseButton(ButtonBehavior, BoxLayout):
    pass


class KBaseToggleButton(ToggleButtonBehavior, BoxLayout):
    pass


class KButton(KBaseButton):
    text = StringProperty()


class KIconButton(KBaseButton):
    icon_text = StringProperty()
    text = StringProperty()


class KToggleButton(KBaseToggleButton):
    text = StringProperty()
