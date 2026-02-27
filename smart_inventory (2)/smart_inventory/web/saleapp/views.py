from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.db import transaction

from .models import Product, Customer, Order, OrderItem
from .forms import ProductForm, CustomerForm

from core.exceptions.exception import OutOfStockException, InvalidQuantityException


# -------------------------
# HOME
# -------------------------
def home(request):
    return render(request, "saleapp/home.html")


# -------------------------
# PRODUCT CRUD
# -------------------------
def product_list(request):
    products = Product.objects.all().order_by("-id")
    return render(request, "saleapp/product_list.html", {"products": products})


def product_create(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("product_list")
    else:
        form = ProductForm()
    return render(request, "saleapp/product_form.html", {"form": form, "mode": "create"})


def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect("product_list")
    else:
        form = ProductForm(instance=product)
    return render(request, "saleapp/product_form.html", {"form": form, "mode": "update", "product": product})


def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        product.delete()
        return redirect("product_list")
    return render(request, "saleapp/product_delete.html", {"product": product})


# -------------------------
# CUSTOMERS
# -------------------------
def customer_register(request):
    if request.method == "POST":
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("customer_list")
    else:
        form = CustomerForm()
    return render(request, "saleapp/customer_register.html", {"form": form})


def customer_list(request):
    customers = Customer.objects.all().order_by("name")
    return render(request, "saleapp/customer_list.html", {"customers": customers})


def customer_find_by_id(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    return render(request, "saleapp/customer_detail.html", {"customer": customer})


# -------------------------
# ORDERS
# -------------------------
def order_create(request):
    customers = Customer.objects.all().order_by("name")
    products = Product.objects.all().order_by("name")

    if request.method == "POST":
        customer_id = request.POST.get("customer_id")

        try:
            if not customer_id:
                raise InvalidQuantityException("Please choose a customer")

            customer = get_object_or_404(Customer, pk=customer_id)

            product_ids = request.POST.getlist("product_id")
            quantities = request.POST.getlist("quantity")

            #  Everything in one DB transaction
            with transaction.atomic():
                order = Order.objects.create(
                    customer=customer,
                    order_date=timezone.now().date()
                )

                added_any_item = False

                for pid, qty in zip(product_ids, quantities):
                    qty_int = int(qty or 0)
                    if not pid or qty_int <= 0:
                        continue

                    product = get_object_or_404(Product, pk=pid)

                    #  Part 1 business-rule style exceptions
                    if qty_int <= 0:
                        raise InvalidQuantityException("Quantity must be positive")

                    if product.quantity_in_stock < qty_int:
                        raise OutOfStockException(
                            f"Not enough stock for {product.name}. "
                            f"Available: {product.quantity_in_stock}, Requested: {qty_int}"
                        )

                    # Save OrderItem
                    OrderItem.objects.create(order=order, product=product, quantity=qty_int)

                    # Update stock
                    product.quantity_in_stock -= qty_int
                    product.save()

                    added_any_item = True

                if not added_any_item:
                    # No selected items => rollback by raising an exception
                    raise InvalidQuantityException("Please select at least one product quantity > 0")

            return redirect("order_history")

        except (OutOfStockException, InvalidQuantityException) as e:
            return render(request, "saleapp/order_form.html", {
                "customers": customers,
                "products": products,
                "error": str(e),
            })

    return render(request, "saleapp/order_form.html", {
        "customers": customers,
        "products": products
    })


def order_history(request):
    orders = (
        Order.objects
        .select_related("customer")
        .prefetch_related("items__product")
        .order_by("-order_date", "-id")
    )
    return render(request, "saleapp/order_history.html", {"orders": orders})


def order_detail(request, pk):
    order = get_object_or_404(
        Order.objects.select_related("customer").prefetch_related("items__product"),
        pk=pk
    )

    # total for your template
    total = sum((it.product.price * it.quantity) for it in order.items.all())

    return render(request, "saleapp/order_detail.html", {"order": order, "total": total})