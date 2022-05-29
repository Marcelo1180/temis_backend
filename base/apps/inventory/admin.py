from django.contrib import admin
from .models import Store
from .models import Order
from .models import ProductOrder

"""
Store
"""
admin.site.register(Store)

"""
Order
"""
admin.site.register(Order)

"""
ProductOrder
"""
admin.site.register(ProductOrder)
