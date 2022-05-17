from django.shortcuts import render
from django.http import JsonResponse
from django.db import transaction
from rest_framework import generics
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view
from .models import Category
from .models import PaymentMethod
from .models import Product
from .models import Order
from .models import ProductOrder
from .serializers import CategorySerializer
from .serializers import ProductSerializer
from .serializers import PaymentMethodSerializer
from .serializers import OrderSerializer
from .structures import SellStructure


@permission_classes([AllowAny])
class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


@permission_classes([AllowAny])
class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filterset_fields = ["category", "available"]


@permission_classes([AllowAny])
class PaymentMethodListView(generics.ListAPIView):
    queryset = PaymentMethod.objects.all()
    serializer_class = PaymentMethodSerializer


@permission_classes([AllowAny])
class OrderCreateView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filterset_fields = ["category", "available"]


@api_view(["POST"])
@permission_classes([AllowAny])
def sell_create(request):
    """
    Sell, ACCESS ROL: ANONYMOUS
    Transction of sell, saving data in ProductOrder and Order tables
    """

    try:
        sell = SellStructure(**request.data)
        order = request.data.get("order", "")
        product_orders = request.data.get("product_orders", "")
        with transaction.atomic():
            order = Order.objects.create_from_json(order)
            ProductOrder.objects.bulk_insert_by_order_from_json(product_orders, order)
        return JsonResponse(request.data, safe=False, status=200)
    except Exception as e:
        return JsonResponse({"message": str(e)}, status=400)
