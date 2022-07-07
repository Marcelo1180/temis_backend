from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
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
    code = models.CharField(max_length=100)
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
    vacuum_packed = models.BooleanField(blank=True, default=False)
    image = models.ImageField(
        upload_to="uploads/", blank=True, default="uploads/default.jpeg"
    )
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
    name = models.CharField(max_length=100, unique=True)
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
