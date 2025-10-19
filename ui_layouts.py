from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.graphics import Rectangle, Color
from kivy.core.window import Window
from ui_controls import *
from app_logic import AuthManager
import db


class AuthScreenLayout(Screen):
    def __init__(self, title_text, show_name_field=True, **kwargs):
        super().__init__(**kwargs)

        self.auth_manager = AuthManager()
        self.show_name_field = show_name_field

        self.osnovnoi_layout = BoxLayout(orientation='vertical', spacing=dp(25), padding=dp(30))

        with self.osnovnoi_layout.canvas.before:
            Color(*COLORS['cream'])
            self.rect = Rectangle(size=Window.size, pos=self.osnovnoi_layout.pos)

        self.osnovnoi_layout.bind(size=self._obnovit_rect, pos=self._obnovit_rect)

        self.zagolovok = ZolotoiNadpis(text=title_text)
        self.osnovnoi_layout.add_widget(self.zagolovok)

        if show_name_field:
            self.pole_imya = ElegantnyiVvod(hint_text='Ваше имя')
            self.osnovnoi_layout.add_widget(self.pole_imya)

        self.pole_telefon = ElegantnyiVvod(hint_text='Номер телефона')
        self.osnovnoi_layout.add_widget(self.pole_telefon)

        self.error_label = Label(
            text='',
            font_size=dp(14),
            color=(0.8, 0.2, 0.2, 1),
            size_hint_y=None,
            height=dp(30)
        )
        self.osnovnoi_layout.add_widget(self.error_label)

        self.knopka_deistvie = ZolotayaKnopka(text='Продолжить')
        self.osnovnoi_layout.add_widget(self.knopka_deistvie)

        self.knopka_nazad = ChernayaKnopka(text='Назад')
        self.knopka_nazad.bind(on_press=self._nazad)
        self.osnovnoi_layout.add_widget(self.knopka_nazad)

        self.add_widget(self.osnovnoi_layout)

    def _obnovit_rect(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos

    def _nazad(self, instance):
        self.manager.current = 'welcome'


class MenuLayout(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.osnovnoi_layout = BoxLayout(orientation='vertical')

        with self.osnovnoi_layout.canvas.before:
            Color(*COLORS['cream'])
            self.rect = Rectangle(size=Window.size, pos=self.osnovnoi_layout.pos)

        self.zagolovok = ZolotoiNadpis(text='Меню ресторана')
        self.osnovnoi_layout.add_widget(self.zagolovok)

        self.scroll = ScrollView()
        self.menu_grid = GridLayout(cols=1, spacing=dp(10), size_hint_y=None)
        self.menu_grid.bind(minimum_height=self.menu_grid.setter('height'))
        self.scroll.add_widget(self.menu_grid)

        self.osnovnoi_layout.add_widget(self.scroll)
        self.add_widget(self.osnovnoi_layout)

    def zagruzit_menu(self):

        menu_items = db.get_menu()
        self.pokazat_menu(menu_items)

    def pokazat_menu(self, menu_items):

        self.menu_grid.clear_widgets()

        for item in menu_items:
            bludo_layout = BoxLayout(
                orientation='horizontal',
                size_hint_y=None,
                height=dp(80),
                padding=dp(10)
            )

            nazvanie = Label(
                text=item[0],
                size_hint_x=0.6,
                color=COLORS['black'],
                bold=True
            )

            cena = Label(
                text=f'{item[1]} руб.',
                size_hint_x=0.4,
                color=COLORS['gold'],
                halign='right'
            )

            bludo_layout.add_widget(nazvanie)
            bludo_layout.add_widget(cena)
            self.menu_grid.add_widget(bludo_layout)