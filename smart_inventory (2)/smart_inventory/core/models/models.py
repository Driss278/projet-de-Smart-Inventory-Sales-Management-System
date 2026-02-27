from core.exceptions.exception import (
    InvalidQuantityException,
    OutOfStockException, InvalidEmailException
)
class Product:
    def __init__(self, id, name, category, price, quantity_in_stock):
        self.id = id
        self.name = name
        self.category = category
        self.price = float(price)
        self.quantity_in_stock = int(quantity_in_stock)

    def add_stock(self, qty: int):
        if qty <= 0:
            raise InvalidQuantityException("Quantity must be positive")
        self.quantity_in_stock += qty
        return f"{qty} items added. New stock: {self.quantity_in_stock}"

    def remove_stock(self, qty: int):
        if qty <= 0:
            raise InvalidQuantityException("Quantity must be positive")
        if qty > self.quantity_in_stock:
            raise OutOfStockException("Not enough stock")
        self.quantity_in_stock -= qty
        return f"{qty} items removed. New stock: {self.quantity_in_stock}"

    def get_value_in_stock(self):
        return self.price * self.quantity_in_stock

    def __str__(self):
        return f"{self.id} {self.name} {self.category} {self.price} {self.quantity_in_stock}"
import re

class Customer:
    def __init__(self, id, name, email):
        self.id = id
        self.name = name
        self.email = email
        self.validate_email()

    def validate_email(self):
        pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
        if not re.match(pattern, self.email):
            raise InvalidEmailException("Invalid email format")
        return True

    def __str__(self):
        return f"{self.id} {self.name} {self.email}"
from datetime import date

class OrderItem:
    def __init__(self, product: Product, quantity: int):
        if quantity <= 0:
            raise InvalidQuantityException("Quantity must be positive")
        self.product = product
        self.quantity = int(quantity)

    def get_subtotal(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"


class Order:
    def __init__(self, id, customer: Customer, order_date=None):
        self.id = id
        self.customer = customer
        self.order_date = order_date or date.today()
        self.items: list[OrderItem] = []

    def add_item(self, product: Product, quantity: int):
        # stock check
        if quantity <= 0:
            raise InvalidQuantityException("Quantity must be positive")
        if product.quantity_in_stock < quantity:
            raise OutOfStockException(f"Not enough stock for {product.name}")

        # update stock + add order item
        product.remove_stock(quantity)
        self.items.append(OrderItem(product, quantity))

    def calculate_total(self):
        return sum(item.get_subtotal() for item in self.items)

    def __str__(self):
        return f"Order({self.id}, {self.customer.name}, {self.order_date}, items={len(self.items)})"  
if __name__ == "__main__":
    p1 = Product(1, "Keyboard", "Electronics", 250, 10)
    p2 = Product(2, "Mouse", "Electronics", 120, 5)

    print("Produits :")
    print(p1)
    print(p2)    
    p1.add_stock(5)
    p2.remove_stock(2)
    print("\nStock après modification :")
    print(p1)
    print(p2)
    c1 = Customer(101, "Driss", "driss@example.com")
    print("\nClient :")
    print(c1)
    order1 = Order(1001, c1)

    order1.add_item(p1, 3)
    order1.add_item(p2, 1)

    print("\nArticles de la commande :")
    for item in order1.items:
      print(item)
    print("\nTotal de la commande :", order1.calculate_total())

    print("\nStock restant :")
    print(p1)
    print(p2)