from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.metrics import dp
from app_logic import AuthManager, CartManager
import db


class WelcomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=dp(50), spacing=dp(20))

        with layout.canvas.before:
            Color(0.98, 0.96, 0.92, 1)
            self.rect = Rectangle(size=Window.size, pos=layout.pos)

        title = Label(
            text='Добро пожаловать!',
            font_size=dp(24),
            color=(0.8, 0.7, 0.4, 1),
            bold=True
        )
        layout.add_widget(title)

        subtitle = Label(
            text='в ресторан "Гурман"',
            font_size=dp(18),
            color=(0.1, 0.1, 0.1, 1)
        )
        layout.add_widget(subtitle)

        login_btn = Button(
            text='Войти',
            size_hint_y=None,
            height=dp(50),
            background_color=(0.8, 0.7, 0.4, 1),
            color=(1, 1, 1, 1)
        )
        login_btn.bind(on_press=self.go_to_login)
        layout.add_widget(login_btn)

        register_btn = Button(
            text='Регистрация',
            size_hint_y=None,
            height=dp(50),
            background_color=(0.1, 0.1, 0.1, 1),
            color=(0.8, 0.7, 0.4, 1)
        )
        register_btn.bind(on_press=self.go_to_register)
        layout.add_widget(register_btn)

        self.add_widget(layout)
        layout.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos

    def go_to_login(self, instance):
        self.manager.current = 'login'

    def go_to_register(self, instance):
        self.manager.current = 'register'


class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=dp(50), spacing=dp(20))

        with layout.canvas.before:
            Color(0.98, 0.96, 0.92, 1)
            self.rect = Rectangle(size=Window.size, pos=layout.pos)

        title = Label(
            text='Вход в аккаунт',
            font_size=dp(24),
            color=(0.8, 0.7, 0.4, 1),
            bold=True
        )
        layout.add_widget(title)

        self.phone_input = TextInput(
            hint_text='Ваш номер телефона',
            size_hint_y=None,
            height=dp(50),
            background_color=(1, 1, 1, 1),
            foreground_color=(0, 0, 0, 1),
            padding=dp(15),
            font_size=dp(16)
        )
        layout.add_widget(self.phone_input)

        self.error_label = Label(
            text='',
            font_size=dp(14),
            color=(0.8, 0.2, 0.2, 1),
            size_hint_y=None,
            height=dp(30)
        )
        layout.add_widget(self.error_label)

        login_btn = Button(
            text='Войти',
            size_hint_y=None,
            height=dp(50),
            background_color=(0.8, 0.7, 0.4, 1),
            color=(1, 1, 1, 1)
        )
        login_btn.bind(on_press=self.login)
        layout.add_widget(login_btn)

        back_btn = Button(
            text='Назад',
            size_hint_y=None,
            height=dp(50),
            background_color=(0.1, 0.1, 0.1, 1),
            color=(0.8, 0.7, 0.4, 1)
        )
        back_btn.bind(on_press=self.go_back)
        layout.add_widget(back_btn)

        self.add_widget(layout)
        layout.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos

    def login(self, instance):
        phone = self.phone_input.text.strip()

        if not phone:
            self.error_label.text = 'Введите номер телефона'
            return

        user = db.get_user_by_phone(phone)
        if not user:
            self.error_label.text = 'Пользователь не найден. Зарегистрируйтесь.'
            return

        auth_mgr = AuthManager()
        if auth_mgr.login(phone):
            self.error_label.text = ''
            self.manager.current = 'main_menu'
        else:
            self.error_label.text = 'Ошибка входа'

    def go_back(self, instance):
        self.manager.current = 'welcome'


class RegisterScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=dp(50), spacing=dp(20))

        with layout.canvas.before:
            Color(0.98, 0.96, 0.92, 1)
            self.rect = Rectangle(size=Window.size, pos=layout.pos)

        title = Label(
            text='Регистрация',
            font_size=dp(24),
            color=(0.8, 0.7, 0.4, 1),
            bold=True
        )
        layout.add_widget(title)

        self.name_input = TextInput(
            hint_text='Ваше имя',
            size_hint_y=None,
            height=dp(50),
            background_color=(1, 1, 1, 1),
            foreground_color=(0, 0, 0, 1),
            padding=dp(15),
            font_size=dp(16)
        )
        layout.add_widget(self.name_input)

        self.phone_input = TextInput(
            hint_text='Номер телефона',
            size_hint_y=None,
            height=dp(50),
            background_color=(1, 1, 1, 1),
            foreground_color=(0, 0, 0, 1),
            padding=dp(15),
            font_size=dp(16)
        )
        layout.add_widget(self.phone_input)

        self.error_label = Label(
            text='',
            font_size=dp(14),
            color=(0.8, 0.2, 0.2, 1),
            size_hint_y=None,
            height=dp(30)
        )
        layout.add_widget(self.error_label)

        register_btn = Button(
            text='Зарегистрироваться',
            size_hint_y=None,
            height=dp(50),
            background_color=(0.8, 0.7, 0.4, 1),
            color=(1, 1, 1, 1)
        )
        register_btn.bind(on_press=self.register)
        layout.add_widget(register_btn)

        back_btn = Button(
            text='Назад',
            size_hint_y=None,
            height=dp(50),
            background_color=(0.1, 0.1, 0.1, 1),
            color=(0.8, 0.7, 0.4, 1)
        )
        back_btn.bind(on_press=self.go_back)
        layout.add_widget(back_btn)

        self.add_widget(layout)
        layout.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos

    def register(self, instance):
        name = self.name_input.text.strip()
        phone = self.phone_input.text.strip()

        if not name:
            self.error_label.text = 'Введите имя'
            return

        if not phone:
            self.error_label.text = 'Введите номер телефона'
            return

        existing_user = db.get_user_by_phone(phone)
        if existing_user:
            self.error_label.text = 'Пользователь с таким номером уже существует'
            return

        auth_mgr = AuthManager()
        if db.save_user(name, phone) and auth_mgr.register(name, phone):
            self.error_label.text = ''
            self.manager.current = 'main_menu'
        else:
            self.error_label.text = 'Ошибка регистрации'

    def go_back(self, instance):
        self.manager.current = 'welcome'


class MainMenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cart_manager = CartManager()
        self.dish_counters = {}

        layout = BoxLayout(orientation='vertical', spacing=dp(10))

        with layout.canvas.before:
            Color(0.98, 0.96, 0.92, 1)
            self.rect = Rectangle(size=Window.size, pos=layout.pos)

        title = Label(
            text='Меню ресторана',
            font_size=dp(24),
            color=(0.8, 0.7, 0.4, 1),
            size_hint_y=0.1,
            bold=True
        )
        layout.add_widget(title)

        self.scroll = ScrollView()
        self.menu_layout = GridLayout(cols=1, spacing=dp(10), size_hint_y=None)
        self.menu_layout.bind(minimum_height=self.menu_layout.setter('height'))

        self.scroll.add_widget(self.menu_layout)
        layout.add_widget(self.scroll)

        bottom_panel = BoxLayout(
            orientation='horizontal',
            size_hint_y=0.12,
            spacing=dp(10),
            padding=dp(10)
        )

        self.cart_btn = Button(
            text='Корзина (0)',
            background_color=(0.8, 0.7, 0.4, 1),
            color=(1, 1, 1, 1)
        )
        self.cart_btn.bind(on_press=self.go_to_cart)

        profile_btn = Button(
            text='Профиль',
            background_color=(0.1, 0.1, 0.1, 1),
            color=(0.8, 0.7, 0.4, 1)
        )
        profile_btn.bind(on_press=self.go_to_profile)

        bottom_panel.add_widget(Label())
        bottom_panel.add_widget(self.cart_btn)
        bottom_panel.add_widget(profile_btn)

        layout.add_widget(bottom_panel)
        self.add_widget(layout)
        layout.bind(size=self._update_rect, pos=self._update_rect)

        Clock.schedule_once(lambda dt: self.load_menu(), 0.1)

    def load_menu(self):
        menu_items = db.get_menu()
        if not menu_items:
            menu_items = [
                ('Тартар из лосося', 890, 'Тартары', 'dish1.jpg'),
                ('Сырная тарелка', 1200, 'Сырные тарелки', 'dish2.jpg'),
                ('Цезарь с креветками', 750, 'Салаты', 'dish3.jpg'),
                ('Стейк рибай', 1500, 'Горячее', 'dish4.jpg'),
                ('Брускетта с томатами', 450, 'Закуски', 'dish5.jpg'),
                ('Тыквенный суп-пюре', 650, 'Супы', 'dish6.jpg'),
                ('Тирамису', 550, 'Десерты', 'dish7.jpg')
            ]
        self.show_menu(menu_items)

    def show_menu(self, menu_items):
        self.menu_layout.clear_widgets()
        self.dish_counters = {}

        for item in menu_items:
            dish_name = item[0]
            self.dish_counters[dish_name] = 0

            dish_box = BoxLayout(
                orientation='horizontal',
                size_hint_y=None,
                height=dp(100),
                padding=dp(10),
                spacing=dp(10)
            )

            try:
                image_path = f"images/{item[3]}" if item[3] else "images/default_dish.jpg"
                image = Image(
                    source=image_path,
                    size_hint_x=0.25,
                    allow_stretch=True
                )
                dish_box.add_widget(image)
            except:
                error_label = Label(
                    text='📷',
                    size_hint_x=0.25,
                    font_size=dp(24)
                )
                dish_box.add_widget(error_label)

            info_box = BoxLayout(orientation='vertical', size_hint_x=0.5)

            name_label = Label(
                text=item[0],
                font_size=dp(16),
                color=(0.1, 0.1, 0.1, 1),
                bold=True,
                size_hint_y=0.6
            )

            price_label = Label(
                text=f'{item[1]} руб. • {item[2]}',
                font_size=dp(14),
                color=(0.8, 0.7, 0.4, 1),
                size_hint_y=0.4
            )

            info_box.add_widget(name_label)
            info_box.add_widget(price_label)
            dish_box.add_widget(info_box)

            controls_box = BoxLayout(
                orientation='horizontal',
                size_hint_x=0.25,
                spacing=dp(5)
            )

            counter_label = Label(
                text='0',
                size_hint_x=0.2,
                font_size=dp(16),
                color=(0.1, 0.1, 0.1, 1),
                bold=True
            )

            minus_btn = Button(
                text='-',
                size_hint_x=0.4,
                background_color=(0.9, 0.8, 0.5, 1)
            )
            minus_btn.bind(on_press=lambda btn, dish=item, counter=counter_label: self.remove_from_cart(dish, counter))

            plus_btn = Button(
                text='+',
                size_hint_x=0.4,
                background_color=(0.8, 0.7, 0.4, 1)
            )
            plus_btn.bind(on_press=lambda btn, dish=item, counter=counter_label: self.add_to_cart(dish, counter))

            controls_box.add_widget(minus_btn)
            controls_box.add_widget(counter_label)
            controls_box.add_widget(plus_btn)

            dish_box.add_widget(controls_box)
            self.menu_layout.add_widget(dish_box)

        self.update_cart_display()

    def add_to_cart(self, dish, counter):
        dish_name = dish[0]
        self.cart_manager.add_item(dish_name, dish[1])
        self.dish_counters[dish_name] += 1
        counter.text = str(self.dish_counters[dish_name])
        self.update_cart_display()

    def remove_from_cart(self, dish, counter):
        dish_name = dish[0]
        if self.dish_counters[dish_name] > 0:
            self.cart_manager.remove_item(dish_name)
            self.dish_counters[dish_name] -= 1
            counter.text = str(self.dish_counters[dish_name])
            self.update_cart_display()

    def update_cart_display(self):
        cart_count = len(self.cart_manager.get_cart_items())
        self.cart_btn.text = f'Корзина ({cart_count})'

    def _update_rect(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos

    def go_to_cart(self, instance):
        self.manager.current = 'cart'

    def go_to_profile(self, instance):
        self.manager.current = 'profile'


class CartScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cart_manager = CartManager()

        layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(10))

        with layout.canvas.before:
            Color(0.98, 0.96, 0.92, 1)
            self.rect = Rectangle(size=Window.size, pos=layout.pos)

        title = Label(
            text='Корзина',
            font_size=dp(24),
            color=(0.8, 0.7, 0.4, 1),
            bold=True
        )
        layout.add_widget(title)

        self.cart_content = Label(
            text='Ваша корзина пуста\n\nДобавьте блюда из меню',
            font_size=dp(16),
            color=(0.5, 0.5, 0.5, 1),
            halign='center'
        )
        layout.add_widget(self.cart_content)

        self.total_label = Label(
            text='Итого: 0 руб.',
            font_size=dp(20),
            color=(0.8, 0.7, 0.4, 1),
            bold=True
        )
        layout.add_widget(self.total_label)

        buttons_box = BoxLayout(orientation='horizontal', spacing=dp(10), size_hint_y=0.15)

        back_btn = Button(
            text='Назад в меню',
            background_color=(0.1, 0.1, 0.1, 1),
            color=(0.8, 0.7, 0.4, 1)
        )
        back_btn.bind(on_press=self.go_back)

        order_btn = Button(
            text='Оформить заказ',
            background_color=(0.8, 0.7, 0.4, 1),
            color=(1, 1, 1, 1)
        )
        order_btn.bind(on_press=self.make_order)

        buttons_box.add_widget(back_btn)
        buttons_box.add_widget(order_btn)
        layout.add_widget(buttons_box)

        self.add_widget(layout)
        layout.bind(size=self._update_rect, pos=self._update_rect)

    def on_enter(self):
        self.show_cart()

    def show_cart(self):
        cart_items = self.cart_manager.get_cart_items()

        if not cart_items:
            self.cart_content.text = 'Ваша корзина пуста\n\nДобавьте блюда из меню'
            self.total_label.text = 'Итого: 0 руб.'
            return

        cart_text = ""
        for item in cart_items:
            cart_text += f"{item['name']} × {item['quantity']}\n"
            cart_text += f"  {item['price']} руб. × {item['quantity']} = {item['price'] * item['quantity']} руб.\n\n"

        self.cart_content.text = cart_text
        self.cart_content.color = (0.1, 0.1, 0.1, 1)
        self.cart_content.halign = 'left'

        total = self.cart_manager.get_total_price()
        self.total_label.text = f'Итого: {total} руб.'

    def _update_rect(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos

    def go_back(self, instance):
        self.manager.current = 'main_menu'

    def make_order(self, instance):
        cart_items = self.cart_manager.get_cart_items()
        if not cart_items:
            return

        auth_mgr = AuthManager()
        user = auth_mgr.get_current_user()

        if user:
            user_db = db.get_user_by_phone(user['phone'])
            if user_db:
                order_data = {
                    'items': cart_items,
                    'total': self.cart_manager.get_total_price()
                }

                if db.save_order(user_db['id'], self.cart_manager.get_total_price(), order_data):
                    print("✅ Заказ сохранен в БД!")

        print("✅ Заказ оформлен!")
        for item in cart_items:
            print(f" - {item['name']} × {item['quantity']}")
        print(f"💰 Сумма: {self.cart_manager.get_total_price()} руб.")

        self.cart_manager.clear_cart()
        self.show_cart()


class ProfileScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(10))

        with layout.canvas.before:
            Color(0.98, 0.96, 0.92, 1)
            self.rect = Rectangle(size=Window.size, pos=layout.pos)

        title = Label(
            text='Профиль',
            font_size=dp(24),
            color=(0.8, 0.7, 0.4, 1),
            bold=True
        )
        layout.add_widget(title)

        self.info_label = Label(
            text='',
            font_size=dp(16),
            color=(0.1, 0.1, 0.1, 1),
            size_hint_y=0.2
        )
        layout.add_widget(self.info_label)

        orders_title = Label(
            text='История заказов:',
            font_size=dp(18),
            color=(0.8, 0.7, 0.4, 1),
            bold=True,
            size_hint_y=0.1
        )
        layout.add_widget(orders_title)

        self.scroll = ScrollView()
        self.orders_layout = GridLayout(cols=1, spacing=dp(10), size_hint_y=None)
        self.orders_layout.bind(minimum_height=self.orders_layout.setter('height'))
        self.scroll.add_widget(self.orders_layout)
        layout.add_widget(self.scroll)

        back_btn = Button(
            text='Назад в меню',
            size_hint_y=None,
            height=dp(50),
            background_color=(0.1, 0.1, 0.1, 1),
            color=(0.8, 0.7, 0.4, 1)
        )
        back_btn.bind(on_press=self.go_back)
        layout.add_widget(back_btn)

        self.add_widget(layout)
        layout.bind(size=self._update_rect, pos=self._update_rect)

    def on_enter(self):
        self.update_profile()

    def update_profile(self):
        auth_mgr = AuthManager()
        user = auth_mgr.get_current_user()

        if user:
            user_info = f"Имя: {user['name']}\nТелефон: {user['phone']}"
            self.info_label.text = user_info
            self.load_user_orders(user['phone'])
        else:
            self.info_label.text = "Войдите в систему"
            self.orders_layout.clear_widgets()

    def load_user_orders(self, phone):
        user_db = db.get_user_by_phone(phone)
        if not user_db:
            return

        orders = db.get_user_orders(user_db['id'])
        self.orders_layout.clear_widgets()

        if not orders:
            no_orders = Label(
                text='У вас пока нет заказов',
                font_size=dp(16),
                color=(0.5, 0.5, 0.5, 1),
                size_hint_y=None,
                height=dp(50)
            )
            self.orders_layout.add_widget(no_orders)
            return

        for order in orders:
            order_box = BoxLayout(
                orientation='vertical',
                size_hint_y=None,
                height=dp(80),
                padding=dp(10)
            )

            order_info = Label(
                text=f'Заказ #{order["id"]} - {order["total_amount"]} руб.',
                font_size=dp(16),
                color=(0.1, 0.1, 0.1, 1),
                bold=True
            )

            order_date = Label(
                text=f'{order["created_at"].strftime("%d.%m.%Y %H:%M")}',
                font_size=dp(14),
                color=(0.5, 0.5, 0.5, 1)
            )

            order_box.add_widget(order_info)
            order_box.add_widget(order_date)
            self.orders_layout.add_widget(order_box)

    def _update_rect(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos

    def go_back(self, instance):
        self.manager.current = 'main_menu'


class MobileMenuApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(WelcomeScreen(name='welcome'))
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(RegisterScreen(name='register'))
        sm.add_widget(MainMenuScreen(name='main_menu'))
        sm.add_widget(CartScreen(name='cart'))
        sm.add_widget(ProfileScreen(name='profile'))
        return sm


if __name__ == '__main__':
    MobileMenuApp().run()