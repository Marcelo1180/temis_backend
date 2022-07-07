from django.shortcuts import render
from .models import Order
from .models import ProductOrder
import pandas as pd


def report_products_by_order(request):
    orders = Order.objects.filter(status="unpaid")
    product_orders = ProductOrder.objects.filter(order__status="unpaid")
    context = {"items": [], "sum_orders": 0}
    if product_orders:
        product_orders = pd.DataFrame(
            product_orders.values("order_id", "product__name", "quantity", "price")
        )
        product_orders["total"] = product_orders["quantity"] * product_orders["price"]
        items = []
        for order in orders:
            products = product_orders.query(f"order_id == {order.id}")
            items.append(
                {
                    "order": order,
                    "products": products[
                        ["product__name", "quantity", "price", "total"]
                    ].to_html(index=False),
                    "products_sum": products["total"].sum(),
                }
            )
            context = {"items": items, "sum_orders": product_orders["total"].sum()}
    return render(request, "products_by_order.html", context)
