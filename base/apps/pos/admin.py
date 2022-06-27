from django.contrib import admin
from .models import CashControl
from .models import Order
from .models import ProductOrder


"""
Order
"""
admin.site.register(Order)

"""
ProductOrder
"""
admin.site.register(ProductOrder)

"""
CashControl
"""
admin.site.register(CashControl)
