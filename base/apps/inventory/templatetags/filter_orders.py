from django import template


register = template.Library()


@register.filter()
def in_order(product_orders, order):
    # print(order.id)
    return product_orders.query(f"order_id == {order.id}")
