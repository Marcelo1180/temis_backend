from django.db import models
from django.conf import settings

class Category(models.Model):
    name = models.CharField(max_length=500)
    sort_by = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name


class ProductUnits(models.TextChoices):
    UNITS = "u", "Units"
    KG = "kg", "Kg"

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=500, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    barcode = models.CharField(max_length=50, blank=True, null=True)
    units = models.CharField(
        max_length=2,
        choices=ProductUnits.choices,
        default=ProductUnits.UNITS,
    )
    available = models.BooleanField(blank=True, default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name


class PaymentMethod(models.Model):
    name = models.CharField(max_length=100)
    sort_by = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Payment method"
        verbose_name_plural = "Payment methods"

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

class Order(models.Model):
    total = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
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
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name = "Product order"
        verbose_name_plural = "Product orders"

    def __str__(self):
        return self.order

    def __unicode__(self):
        return self.order
