from django import forms
from .models import Product, Customer, Order, OrderItem

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name","category", "price", "quantity_in_stock"]

    # Custom validation
    def clean_price(self):
        price = self.cleaned_data["price"]
        if price <= 0:
            raise forms.ValidationError("Price must be greater than 0.")
        return price

    def clean_stock(self):
        stock = self.cleaned_data["stock"]
        if stock < 0:
            raise forms.ValidationError("Stock cannot be negative.")
        return stock


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ["name", "email"]

    def clean_email(self):
        email = self.cleaned_data["email"]
        if Customer.objects.filter(email=email).exists():
            raise forms.ValidationError("This email already exists.")
        return email


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["customer"]  # only customer, date is auto-added

class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ["product", "quantity"]

    def clean_quantity(self):
        q = self.cleaned_data["quantity"]
        if q <= 0:
            raise forms.ValidationError("Quantity must be greater than 0.")
        return q
from django import forms
from .models import Customer

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ["name", "email"]

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        if Customer.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already used.")
        return email


