# setup_complete.py
import sqlite3

def setup_database():
    conn = sqlite3.connect('ecommerce.db')
    cursor = conn.cursor()
    
    print("="*60)
    print("ПОЛНАЯ НАСТРОЙКА БАЗЫ ДАННЫХ ECOMMERCE")
    print("="*60)
    
    try:
        print("\n1️⃣  УДАЛЕНИЕ СТАРЫХ ТАБЛИЦ...")
        cursor.execute("DROP TABLE IF EXISTS products;")
        cursor.execute("DROP TABLE IF EXISTS categories;")
        print("✅ Старые таблицы удалены")
        
        print("\n2️⃣  СОЗДАНИЕ НОВЫХ ТАБЛИЦ...")
        # Таблица categories
        cursor.execute('''
        CREATE TABLE categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            description TEXT
        )
        ''')
        
        # Таблица products
        cursor.execute('''
        CREATE TABLE products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            price REAL NOT NULL,
            image_url TEXT,
            stock_quantity INTEGER DEFAULT 0,
            category_id INTEGER,
            FOREIGN KEY (category_id) REFERENCES categories (id)
        )
        ''')
        
        # Индексы
        cursor.execute('CREATE INDEX ix_categories_id ON categories (id)')
        cursor.execute('CREATE INDEX ix_products_id ON products (id)')
        print("✅ Таблицы созданы")
        
        print("\n3️⃣  ДОБАВЛЕНИЕ КАТЕГОРИЙ...")
        categories = [
            ("Электроника", "Гаджеты и электронные устройства"),
            ("Компьютеры", "Компьютеры и комплектующие"),
            ("Бытовая техника", "Техника для дома"),
            ("Смартфоны", "Мобильные телефоны и аксессуары"),
        ]
        
        cursor.executemany("INSERT INTO categories (name, description) VALUES (?, ?)", categories)
        print(f"✅ Добавлено {len(categories)} категорий")
        
        print("\n4️⃣  ДОБАВЛЕНИЕ ТОВАРОВ...")
        products = [
            ("Ноутбук ASUS VivoBook", "15.6-дюймовый ноутбук с процессором Intel Core i5", 54999.99, None, 15, 2),
            ("Смартфон Samsung Galaxy S23", "Флагманский смартфон с камерой 108 МП", 79999.99, None, 25, 4),
            ("Телевизор LG OLED 55''", "4K OLED телевизор с технологией HDR", 89999.99, None, 8, 1),
            ("Холодильник Bosch", "Двухкамерный холодильник с системой No Frost", 64999.99, None, 12, 3),
            ("Наушники Sony WH-1000XM5", "Беспроводные наушники с шумоподавлением", 29999.99, None, 30, 1),
            ("Игровая приставка PlayStation 5", "Новейшая игровая консоль от Sony", 54999.99, None, 5, 1),
            ("Стиральная машина Indesit", "Стиральная машина с загрузкой 7 кг", 27999.99, None, 18, 3),
            ("Монитор Dell 27''", "Монитор с разрешением 2560x1440, 144 Гц", 32999.99, None, 22, 2),
        ]
        
        cursor.executemany(
            """INSERT INTO products (name, description, price, image_url, stock_quantity, category_id) 
               VALUES (?, ?, ?, ?, ?, ?)""",
            products
        )
        print(f"✅ Добавлено {len(products)} товаров")
        
        conn.commit()
        
        print("\n" + "="*60)
        print("✅ БАЗА ДАННЫХ УСПЕШНО НАСТРОЕНА!")
        print("="*60)
        
        # Итоговая статистика
        cursor.execute("SELECT COUNT(*) FROM categories;")
        cat_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM products;")
        prod_count = cursor.fetchone()[0]
        
        print(f"\n📊 СТАТИСТИКА:")
        print(f"   Категорий: {cat_count}")
        print(f"   Товаров: {prod_count}")
        
        print("\n📋 КАТЕГОРИИ:")
        cursor.execute("SELECT id, name FROM categories ORDER BY id;")
        for row in cursor.fetchall():
            print(f"   {row[0]}. {row[1]}")
        
        print("\n🛒 ПЕРВЫЕ 5 ТОВАРОВ:")
        cursor.execute("SELECT id, name, price FROM products ORDER BY id LIMIT 5;")
        for row in cursor.fetchall():
            print(f"   {row[0]}. {row[1]:30} - {row[2]:8.2f} руб.")
        
    except Exception as e:
        print(f"\n❌ ОШИБКА: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    setup_database()