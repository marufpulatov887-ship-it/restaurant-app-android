import json
import psycopg2
import sqlite3
from kivy import platform



def is_mobile():
    return platform in ('android', 'ios')


def get_connection():
    try:
        if is_mobile():
            # SQLite для мобильных
            conn = sqlite3.connect('restaurant.db')
            init_sqlite_database(conn)
            return conn
        else:
            # PostgreSQL для ПК
            conn = psycopg2.connect(
                host="localhost",
                database="restaurant1",
                user="postgres",
                password="1"
            )
            return conn
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")
        return None


def init_sqlite_database(conn):
    """Инициализация SQLite базы при первом запуске на мобильном"""
    try:
        cur = conn.cursor()

        # Таблица пользователей
        cur.execute('''
            CREATE TABLE IF NOT EXISTS app_users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT UNIQUE NOT NULL
            )
        ''')


        cur.execute('''
            CREATE TABLE IF NOT EXISTS menu_items (
                name TEXT,
                price REAL,
                category TEXT, 
                image_path TEXT
            )
        ''')

        # Таблица заказов
        cur.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                total_amount REAL NOT NULL,
                order_data TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Проверяем есть ли данные в меню
        cur.execute("SELECT COUNT(*) FROM menu_items")
        if cur.fetchone()[0] == 0:
            # Добавляем тестовые данные
            menu_data = [
                ('Тартар из лосося', 890, 'Тартары', 'images/dish1.jpg'),
                ('Сырная тарелка', 1200, 'Сырные тарелки', 'images/dish2.jpg'),
                ('Цезарь с креветками', 750, 'Салаты', 'images/dish3.jpg'),
                ('Стейк рибай', 1500, 'Горячее', 'images/dish4.jpg'),
                ('Брускетта с томатами', 450, 'Закуски', 'images/dish5.jpg'),
                ('Тыквенный суп-пюре', 650, 'Супы', 'images/dish6.jpg'),
                ('Тирамису', 550, 'Десерты', 'images/dish7.jpg')
            ]
            cur.executemany(
                "INSERT INTO menu_items (name, price, category, image_path) VALUES (?, ?, ?, ?)",
                menu_data
            )

        conn.commit()
    except Exception as e:
        print(f"❌ Ошибка инициализации SQLite: {e}")


# ВСЕ ОСТАЛЬНЫЕ ФУНКЦИИ ОСТАЮТСЯ БЕЗ ИЗМЕНЕНИЙ!
def save_user(name, phone):
    conn = get_connection()
    if conn is None:
        return False

    try:
        cur = conn.cursor()
        if is_mobile():
            cur.execute(
                "INSERT INTO app_users (name, phone) VALUES (?, ?)",
                (name, phone)
            )
        else:
            cur.execute(
                "INSERT INTO app_users (name, phone) VALUES (%s, %s)",
                (name, phone)
            )
        conn.commit()
        cur.close()
        if not is_mobile():
            conn.close()
        return True
    except Exception as e:
        print(f"❌ Ошибка сохранения: {e}")
        return False


def get_user_by_phone(phone):
    conn = get_connection()
    if conn is None:
        return None

    try:
        cur = conn.cursor()
        if is_mobile():
            cur.execute("SELECT id, name, phone FROM app_users WHERE phone = ?", (phone,))
        else:
            cur.execute("SELECT id, name, phone FROM app_users WHERE phone = %s", (phone,))
        user = cur.fetchone()
        cur.close()
        if not is_mobile():
            conn.close()

        if user:
            return {'id': user[0], 'name': user[1], 'phone': user[2]}
        return None
    except Exception as e:
        print(f"❌ Ошибка поиска пользователя: {e}")
        return None


def get_menu():
    conn = get_connection()
    if conn is None:
        return []

    try:
        cur = conn.cursor()
        cur.execute("SELECT DISTINCT name, price, category, image_path FROM menu_items")
        menu_items = cur.fetchall()
        cur.close()
        if not is_mobile():
            conn.close()
        return menu_items
    except Exception as e:
        print(f"❌ Ошибка загрузки меню: {e}")
        return []


def save_order(user_id, total_amount, order_data):
    conn = get_connection()
    if conn is None:
        return False

    try:
        cur = conn.cursor()
        if is_mobile():
            cur.execute(
                "INSERT INTO orders (user_id, total_amount, order_data) VALUES (?, ?, ?)",
                (user_id, total_amount, json.dumps(order_data))
            )
        else:
            cur.execute(
                "INSERT INTO orders (user_id, total_amount, order_data) VALUES (%s, %s, %s)",
                (user_id, total_amount, json.dumps(order_data))
            )
        conn.commit()
        cur.close()
        if not is_mobile():
            conn.close()
        return True
    except Exception as e:
        print(f"❌ Ошибка сохранения заказа: {e}")
        return False


def get_user_orders(user_id):
    conn = get_connection()
    if conn is None:
        return []

    try:
        cur = conn.cursor()
        if is_mobile():
            cur.execute(
                "SELECT id, total_amount, order_data, created_at FROM orders WHERE user_id = ? ORDER BY created_at DESC",
                (user_id,))
        else:
            cur.execute(
                "SELECT id, total_amount, order_data, created_at FROM orders WHERE user_id = %s ORDER BY created_at DESC",
                (user_id,))
        orders = cur.fetchall()
        cur.close()
        if not is_mobile():
            conn.close()

        order_list = []
        for order in orders:
            order_list.append({
                'id': order[0],
                'total_amount': order[1],
                'order_data': order[2],
                'created_at': order[3]
            })
        return order_list
    except Exception as e:
        print(f"❌ Ошибка загрузки заказов: {e}")
        return []


def search_dishes(query):
    menu_items = get_menu()
    results = [item for item in menu_items if query.lower() in item[0].lower()]
    return results