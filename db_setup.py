import sqlite3


def setup_database():
    conn = sqlite3.connect("retail.db")
    cursor = conn.cursor()

    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS households
                   (
                       hshd_num
                       INTEGER,
                       loyalty_flag
                       TEXT,
                       age_range
                       TEXT,
                       income_range
                       TEXT,
                       presence_of_children
                       TEXT
                   )
                   ''')

    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS transactions
                   (
                       hshd_num
                       INTEGER,
                       basket_num
                       INTEGER,
                       date
                       TEXT,
                       product_num
                       INTEGER,
                       spend
                       FLOAT,
                       units
                       INTEGER,
                       store_region
                       TEXT
                   )
                   ''')

    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS products
                   (
                       product_num
                       INTEGER,
                       department
                       TEXT,
                       commodity
                       TEXT,
                       brand_type
                       TEXT,
                       natural_organic_flag
                       TEXT
                   )
                   ''')

    conn.commit()
    conn.close()


if __name__ == "__main__":
    setup_database()
