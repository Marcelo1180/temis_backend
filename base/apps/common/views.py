from django.shortcuts import render
from rest_framework import generics
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Category
from .models import PaymentMethod
from .models import Product
from .serializers import CategorySerializer
from .serializers import ProductSerializer
from .serializers import PaymentMethodSerializer


@permission_classes([IsAuthenticated])
class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


@permission_classes([IsAuthenticated])
class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filterset_fields = ["category", "available"]


@permission_classes([IsAuthenticated])
class PaymentMethodListView(generics.ListAPIView):
    queryset = PaymentMethod.objects.all()
    serializer_class = PaymentMethodSerializer
