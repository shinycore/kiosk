import weakref

from kivy.animation import Animation
from kivy.properties import NumericProperty, StringProperty
from kivy.uix.modalview import ModalView
from kivy.uix.widget import Widget


class KProgressIndicator(Widget):
    angle = NumericProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        animation = Animation(angle=180, duration=1) + Animation(angle=360, duration=1)
        animation.repeat = True
        animation.start(self)

    @staticmethod
    def on_angle(item: Widget, angle: int):
        if angle == 360:
            item.angle = 0


class KBasePopup(ModalView):
    prev = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        ref = KBasePopup.prev  # no walruses in 3.7
        if ref:
            modal: "KBasePopup" = ref()
            if modal:
                modal.dismiss()

        KBasePopup.prev = weakref.ref(self)


class KLoadingPopup(KBasePopup):
    text = StringProperty()


class KStatusPopup(KBasePopup):
    text = StringProperty()
