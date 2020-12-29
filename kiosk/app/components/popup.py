import weakref

from kivy.properties import StringProperty
from kivy.uix.modalview import ModalView


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


class KStatusPopup(KBasePopup):
    text = StringProperty()
