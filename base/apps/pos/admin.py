from django.contrib import admin
from .models import CashControl
from .models import Category
from .models import Order
from .models import ProductOrder
from .models import Product
from .models import PaymentMethod

"""
Category
"""
admin.site.register(Category)

"""
Order
"""
admin.site.register(Order)

"""
ProductOrder
"""
admin.site.register(ProductOrder)

"""
Product
"""
admin.site.register(Product)

"""
PaymentMethod
"""
admin.site.register(PaymentMethod)

"""
CashControl
"""
admin.site.register(CashControl)
