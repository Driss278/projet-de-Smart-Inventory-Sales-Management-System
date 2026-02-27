from datetime import date

from core.models.order import Order
from core.models.order_item import OrderItem
from core.exceptions.exception import (
    OutOfStockException,
    InvalidQuantityException,InvalidQuantityException
)


class OrderService:
    """
    Business service responsible for order creation logic.
    Independent from Django and database.
    """

    def create_order(self, order_id, customer, products_with_qty):
        """
        :param order_id: int or None
        :param customer: core.models.customer.Customer
        :param products_with_qty: list of tuples (Product, quantity)
        :return: Order (core domain object)
        """

        order = Order(
            id=order_id,
            customer=customer,
            order_date=date.today()
        )

        added_any_item = False

        for product, qty in products_with_qty:
            if qty <= 0:
                continue  # ignore zero quantities

            # 🔥 Business rules
            if qty <= 0:
                raise InvalidQuantityException("Quantity must be greater than zero")

            if product.quantity_in_stock < qty:
                raise OutOfStockException(
                    f"Product '{product.name}' has only "
                    f"{product.quantity_in_stock} items available"
                )

            # Update stock + add item
            product.remove_stock(qty)
            order.items.append(OrderItem(product, qty))
            added_any_item = True

        if not added_any_item:
            raise InvalidQuantityException(
                "Order must contain at least one product with quantity > 0"
            )

        return order