# fill_data_simple.py
import sqlite3

def fill_database():
    conn = sqlite3.connect('ecommerce.db')
    cursor = conn.cursor()
    
    print("🔄 Проверка и заполнение базы данных...")
    
    # Проверяем существуют ли таблицы
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='categories';")
    if not cursor.fetchone():
        print("❌ Таблицы не созданы! Сначала запустите create_tables.py")
        return
    
    try:
        print("\n📂 Добавление категорий...")
        # Добавим категории
        categories = [
            ("Электроника", "Гаджеты и электронные устройства"),
            ("Компьютеры", "Компьютеры и комплектующие"),
            ("Бытовая техника", "Техника для дома"),
            ("Смартфоны", "Мобильные телефоны и аксессуары"),
        ]
        
        cursor.executemany(
            "INSERT INTO categories (name, description) VALUES (?, ?)",
            categories
        )
        print(f"✅ Добавлено {len(categories)} категорий")
        
        print("\n📦 Добавление товаров...")
        # Добавим товары
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
            """INSERT INTO products 
               (name, description, price, image_url, stock_quantity, category_id) 
               VALUES (?, ?, ?, ?, ?, ?)""",
            products
        )
        print(f"✅ Добавлено {len(products)} товаров")
        
        conn.commit()
        
        # Финальная проверка
        print("\n✅ ФИНАЛЬНАЯ ПРОВЕРКА:")
        
        cursor.execute("SELECT COUNT(*) FROM categories;")
        cat_count = cursor.fetchone()[0]
        print(f"📊 Категорий в базе: {cat_count}")
        
        cursor.execute("SELECT COUNT(*) FROM products;")
        prod_count = cursor.fetchone()[0]
        print(f"📊 Товаров в базе: {prod_count}")
        
        # Покажем список
        print("\n📋 Категории:")
        cursor.execute("SELECT id, name FROM categories ORDER BY id;")
        for row in cursor.fetchall():
            print(f"  {row[0]}. {row[1]}")
        
        print("\n🛒 Товары:")
        cursor.execute("SELECT id, name, price FROM products ORDER BY id;")
        for row in cursor.fetchall():
            print(f"  {row[0]}. {row[1]:30} - {row[2]:8.2f} руб.")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    print("=" * 50)
    print("ЗАПОЛНЕНИЕ БАЗЫ ДАННЫХ ECOMMERCE")
    print("=" * 50)
    fill_database()