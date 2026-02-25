# create_tables.py
import sqlite3

def create_tables():
    conn = sqlite3.connect('ecommerce.db')
    cursor = conn.cursor()
    
    print("🔄 Создание таблиц...")
    
    # Удаляем старые таблицы если они есть
    cursor.execute("DROP TABLE IF EXISTS products;")
    cursor.execute("DROP TABLE IF EXISTS categories;")
    
    # Создаем таблицу categories
    cursor.execute('''
    CREATE TABLE categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        description TEXT
    )
    ''')
    print("✅ Таблица 'categories' создана")
    
    # Создаем таблицу products
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
    print("✅ Таблица 'products' создана")
    
    # Создаем индексы
    cursor.execute('CREATE INDEX ix_categories_id ON categories (id)')
    cursor.execute('CREATE INDEX ix_products_id ON products (id)')
    print("✅ Индексы созданы")
    
    conn.commit()
    conn.close()
    print("✅ Все таблицы успешно созданы!")

if __name__ == "__main__":
    print("="*50)
    print("СОЗДАНИЕ ТАБЛИЦ БАЗЫ ДАННЫХ")
    print("="*50)
    create_tables()