
from django.urls import path
from . import views

from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),

    # PRODUCTS
    path("products/", views.product_list, name="product_list"),
    path("products/add/", views.product_create, name="product_create"),
    path("products/<int:pk>/edit/", views.product_update, name="product_update"),
    path("products/<int:pk>/delete/", views.product_delete, name="product_delete"),

    # CUSTOMERS
    path("customers/", views.customer_list, name="customer_list"),
    path("customers/register/", views.customer_register, name="customer_register"),
    path("customers/<int:pk>/", views.customer_find_by_id, name="customer_find_by_id"),
    path("orders/add/", views.order_create, name="order_create"),
    path("orders/", views.order_history, name="order_history"),
    path("orders/<int:pk>/", views.order_detail, name="order_detail"),
]



