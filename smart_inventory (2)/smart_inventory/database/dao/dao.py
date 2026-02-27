from mysql.connector import Error
import mysql.connector
from core.models.models import Product
from core.models.modelsr import Customer
from core.models.models import Order
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",      # adapte
    database="productmanagement"
)



class ProductDAO:
    def save(self, conn, product: Product):
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO saleapp_products (id, name, category, price, quantity_in_stock)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (product.id, product.name, product.category, product.price, product.quantity_in_stock)
            )
            conn.commit()
        except Error as e:
            conn.rollback()
            raise e

    def update(self, conn, product: Product):
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE saleapp_products
                SET name=%s, category=%s, price=%s, quantity_in_stock=%s
                WHERE id=%s
                """,
                (product.name, product.category, product.price, product.quantity_in_stock, product.id)
            )
            conn.commit()
        except Error as e:
            conn.rollback()
            raise e

    def delete(self, conn, product_id):
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM saleapp_products WHERE id=%s", (product_id,))
            conn.commit()
        except Error as e:
            conn.rollback()
            raise e

    def find_by_id(self, conn, product_id):
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM saleapp_products WHERE id=%s", (product_id,))
        row = cursor.fetchone()
        if not row:
            return None
        return Product(row["id"], row["name"], row["category"], row["price"], row["quantity_in_stock"])
class OrderDAO:
    def save(self, conn, order: Order):
        try:
            cursor = conn.cursor()

            # 1) insert order
            cursor.execute(
                "INSERT INTO saleapp_orders (id, customer_id, order_date) VALUES (%s, %s, %s)",
                (order.id, order.customer.id, order.order_date)
            )

            # 2) insert items
            for item in order.items:
                cursor.execute(
                    "INSERT INTO saleapp_orderitems (order_id, product_id, quantity) VALUES (%s, %s, %s)",
                    (order.id, item.product.id, item.quantity)
                )

            conn.commit()
        except Error as e:
            conn.rollback()
            raise e

    def find_by_id(self, conn, order_id):
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM saleapp_orders WHERE id=%s", (order_id,))
        order_row = cursor.fetchone()
        if not order_row:
            return None

        # load customer
        customer_dao = CustomerDAO()
        customer = customer_dao.find_by_id(conn, order_row["customer_id"])

        order = Order(order_row["id"], customer, order_row["order_date"])

        # load items
        cursor.execute("SELECT * FROM saleapp_orderitems WHERE order_id=%s", (order_id,))
        items_rows = cursor.fetchall()

        product_dao = ProductDAO()
        for r in items_rows:
            product = product_dao.find_by_id(conn, r["product_id"])
            order.items.append(OrderItem(product, r["quantity"]))

        return order
class CustomerDAO:
    def save(self, conn, customer: Customer):
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO saleapp_customers (id, name, email) VALUES (%s, %s, %s)",
                (customer.id, customer.name, customer.email)
            )
            conn.commit()
        except Error as e:
            conn.rollback()
            raise e

    def update(self, conn, customer: Customer):
        try:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE saleapp_customers SET name=%s, email=%s WHERE id=%s",
                (customer.name, customer.email, customer.id)
            )
            conn.commit()
        except Error as e:
            conn.rollback()
            raise e

    def delete(self, conn, customer_id):
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM saleapp_customers WHERE id=%s", (customer_id,))
            conn.commit()
        except Error as e:
            conn.rollback()
            raise e

    def find_by_id(self, conn, customer_id):
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM customers WHERE id=%s", (customer_id,))
        row = cursor.fetchone()
        if not row:
            return None
        return Customer(row["id"], row["name"], row["email"])


