import mysql.connector

def init_db():
    """Ensure the orders table exists with unique order_id."""
    conn = mysql.connector.connect(
        host="mysql",
        user="root",
        password="root",
        database="payments"
    )
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INT AUTO_INCREMENT PRIMARY KEY,
            order_id INT UNIQUE,   -- ✅ unique constraint
            item VARCHAR(100),
            price INT
        )
    """)
    conn.commit()
    conn.close()

def get_all_orders():
    conn = mysql.connector.connect(
        host="mysql",
        user="root",
        password="root",
        database="payments"
    )
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT order_id, item, price FROM orders")

    results = cursor.fetchall()

    conn.close()

    return results

def save_payment(order):
    """Insert order into DB, skip duplicates."""
    conn = mysql.connector.connect(
        host="mysql",
        user="root",
        password="root",
        database="payments"
    )
    cursor = conn.cursor()
    try:
        query = "INSERT INTO orders (order_id, item, price) VALUES (%s, %s, %s)"
        cursor.execute(query, (order["order_id"], order["item"], order["price"]))
        conn.commit()
    except mysql.connector.Error as e:
        print("DB insert failed:", e)  # e.g. duplicate order_id
    finally:
        conn.close()