import logging
from django.conf import settings
from django.db import models
from django.db import IntegrityError, transaction
from django.contrib.auth.models import User


logger = logging.getLogger(__name__)


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
    image = models.ImageField(upload_to="uploads/", blank=True, null=True)
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

class OrderManager(models.Manager):
    def create_from_json(self, order):
        payment_method = PaymentMethod.objects.get(id=order.pop("payment_method"))
        author = User.objects.get(id=order.pop("author"))
        return Order.objects.create(**order, payment_method=payment_method, author=author)

class Order(models.Model):
    total = models.DecimalField(decimal_places=2, max_digits=10)
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = OrderManager()

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"

    def __str__(self):
        return f"Order #{self.id}"

    def __unicode__(self):
        return f"Order #{self.id}"


class ProductOrderManager(models.Manager):
    def bulk_insert_by_order_from_json(self, product_orders, order):
        try:
            with transaction.atomic():
                for product_order in product_orders:
                    product = Product.objects.get(id=product_order.pop("product"))
                    ProductOrder.objects.create(
                        **product_order, product=product, order=order
                    )
        except IntegrityError as err:
            logger.error(f"Bulk upsert failed: {err}")


class ProductOrder(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.DecimalField(decimal_places=2, max_digits=10)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = ProductOrderManager()

    class Meta:
        verbose_name = "Product order"
        verbose_name_plural = "Product orders"

    def __str__(self):
        return f"Order product: #{self.id}"

    def __unicode__(self):
        return f"Order product: #{self.id}"

class CashControl(models.Model):
    total = models.DecimalField(decimal_places=2, max_digits=10)
    date = models.DateField()
    sales = models.IntegerField(default=0)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    detail = models.TextField()
    observation = models.TextField(default="")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Cash control"
        verbose_name_plural = "Cash controls"

    def __str__(self):
        return f"Cash control #{self.id}"

    def __unicode__(self):
        return f"Cash control #{self.id}"
