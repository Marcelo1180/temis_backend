from django.contrib import admin
from .models import Category
from .models import Product
from .models import PaymentMethod


"""
Category
"""
admin.site.register(Category)

"""
Product
"""


class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "image", "barcode", "code", "available", "vacuum_packed")


admin.site.register(Product, ProductAdmin)

"""
PaymentMethod
"""
admin.site.register(PaymentMethod)
