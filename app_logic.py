from kivy.storage.jsonstore import JsonStore
import db


class AuthManager:
    def __init__(self):
        self.store = JsonStore('auth.json')
        self.current_user = None

    def register(self, name, phone):
        self.store.put('user', name=name, phone=phone, logged_in=True)
        self.current_user = {'name': name, 'phone': phone}
        return True

    def login(self, phone):
        user = db.get_user_by_phone(phone)
        if user:
            self.store.put('user', name=user['name'], phone=user['phone'], logged_in=True)
            self.current_user = user
            return True
        return False

    def is_logged_in(self):
        return self.store.exists('user')

    def get_current_user(self):
        if self.store.exists('user'):
            user_data = self.store.get('user')
            return {'name': user_data.get('name'), 'phone': user_data.get('phone')}
        return None

    def logout(self):
        self.store.delete('user')
        self.current_user = None


cart_items = []


class CartManager:
    def __init__(self):
        global cart_items
        self.items = cart_items

    def add_item(self, dish_name, price):
        for item in self.items:
            if item['name'] == dish_name:
                item['quantity'] += 1
                return

        self.items.append({
            'name': dish_name,
            'price': price,
            'quantity': 1
        })

    def remove_item(self, dish_name):
        for item in self.items:
            if item['name'] == dish_name:
                if item['quantity'] > 1:
                    item['quantity'] -= 1
                else:
                    self.items.remove(item)
                return True
        return False

    def get_cart_items(self):
        return self.items

    def get_total_price(self):
        return sum(item['price'] * item['quantity'] for item in self.items)

    def clear_cart(self):
        self.items.clear()