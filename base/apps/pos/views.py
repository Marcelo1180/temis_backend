from django.shortcuts import render
from rest_framework import generics
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from .models import Category
from .models import Product
from .serializers import CategorySerializer
from .serializers import ProductSerializer


@permission_classes([AllowAny])
class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


@permission_classes([AllowAny])
class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filterset_fields = ['category', 'available']
