import mysql.connector

def init_db(config):
    conn = mysql.connector.connect(
        host=config["MYSQL_HOST"],
        user=config["MYSQL_USER"],
        password=config["MYSQL_PASSWORD"],
        database=config["MYSQL_DB"]
    )

    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INT AUTO_INCREMENT PRIMARY KEY,
            order_id INT UNIQUE,
            item VARCHAR(100),
            price INT
        )
    """)
    conn.commit()
    conn.close()


def get_all_orders(config):
    conn = mysql.connector.connect(
        host=config["MYSQL_HOST"],
        user=config["MYSQL_USER"],
        password=config["MYSQL_PASSWORD"],
        database=config["MYSQL_DB"]
    )
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT order_id, item, price FROM orders")
    results = cursor.fetchall()
    conn.close()
    return results


def save_payment(order, config):
    conn = mysql.connector.connect(
        host=config["MYSQL_HOST"],
        user=config["MYSQL_USER"],
        password=config["MYSQL_PASSWORD"],
        database=config["MYSQL_DB"]
    )
    cursor = conn.cursor()
    try:
        query = "INSERT INTO orders (order_id, item, price) VALUES (%s, %s, %s)"
        cursor.execute(query, (order["order_id"], order["item"], order["price"]))
        conn.commit()
    except mysql.connector.Error as e:
        print("DB insert failed:", e)
    finally:
        conn.close()