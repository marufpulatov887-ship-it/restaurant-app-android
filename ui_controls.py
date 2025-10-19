from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.graphics import Color, RoundedRectangle
from kivy.metrics import dp

COLORS = {
    'black': (0.1, 0.1, 0.1, 1),
    'gold': (0.8, 0.7, 0.4, 1),
    'light_gold': (0.9, 0.85, 0.7, 1),
    'cream': (0.98, 0.96, 0.92, 1),
    'dark_gray': (0.2, 0.2, 0.2, 1),
    'white': (1, 1, 1, 1),
}


class ZolotayaKnopka(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_color = (0, 0, 0, 0)
        self.color = COLORS['black']
        self.font_size = dp(16)
        self.size_hint_y = None
        self.height = dp(50)
        self.bold = True

        with self.canvas.before:
            Color(*COLORS['gold'])
            self.rect = RoundedRectangle(size=self.size, pos=self.pos, radius=[dp(10)])

        self.bind(pos=self._obnovit_rect, size=self._obnovit_rect)

    def _obnovit_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size


class ChernayaKnopka(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_color = (0, 0, 0, 0)
        self.color = COLORS['gold']
        self.font_size = dp(16)
        self.size_hint_y = None
        self.height = dp(50)

        with self.canvas.before:
            Color(*COLORS['black'])
            self.rect = RoundedRectangle(size=self.size, pos=self.pos, radius=[dp(10)])

        self.bind(pos=self._obnovit_rect, size=self._obnovit_rect)

    def _obnovit_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size


class ZolotoiNadpis(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.color = COLORS['gold']
        self.font_size = dp(24)
        self.bold = True
        self.size_hint_y = None
        self.height = dp(60)


class TemnyiNadpis(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.color = COLORS['black']
        self.font_size = dp(18)
        self.size_hint_y = None
        self.height = dp(40)


class ElegantnyiVvod(TextInput):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_color = COLORS['white']
        self.foreground_color = COLORS['black']
        self.font_size = dp(16)
        self.size_hint_y = None
        self.height = dp(50)
        self.padding = [dp(15), dp(15)]
        self.hint_text_color = [0.5, 0.5, 0.5, 1]

        self.cursor_color = COLORS['black']

        with self.canvas.before:
            Color(*COLORS['gold'])
            self.rect = RoundedRectangle(size=self.size, pos=self.pos, radius=[dp(8)])

        self.bind(pos=self._obnovit_rect, size=self._obnovit_rect)

    def _obnovit_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = (instance.size[0], instance.size[1])