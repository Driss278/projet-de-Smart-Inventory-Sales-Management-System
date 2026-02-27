class OutOfStockException(Exception):
    def __init__(self, message="Not enough stock available"):
        super().__init__(message)


class InvalidEmailException(Exception):
    def __init__(self, message="Invalid email address"):
        super().__init__(message)


class InvalidQuantityException(Exception):
    def __init__(self, message="Quantity must be greater than zero"):
        super().__init__(message)