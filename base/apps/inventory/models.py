from django.db import models
from django.conf import settings
from base.apps.common.models import Product


class Store(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Store"
        verbose_name_plural = "Stores"

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

class Order(models.Model):
    total = models.DecimalField(decimal_places=2, max_digits=10)
    from_store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name="invetory_from_store")
    to_store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name="inventory_to_store")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="inventory_order_author")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"

    def __str__(self):
        return f"Order #{self.id}"

    def __unicode__(self):
        return f"Order #{self.id}"


class ProductOrder(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="inventory_product_order")
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.DecimalField(decimal_places=2, max_digits=10)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Product order"
        verbose_name_plural = "Product orders"

    def __str__(self):
        return f"Order product: #{self.id}"

    def __unicode__(self):
        return f"Order product: #{self.id}"
