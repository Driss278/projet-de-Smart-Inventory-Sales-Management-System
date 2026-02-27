from django.contrib import admin
from .models import Product, Customer, Order, OrderItem

admin.site.register([Product, Customer, Order, OrderItem])
# Register your models here.


# Inline to show OrderItems inside an Order
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1  # how many empty slots to show

# Order admin with inline OrderItems


