import datetime
import json
from django.shortcuts import render
from django.http import JsonResponse
from django.db import transaction
from rest_framework import generics
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from .models import CashControl, Category
from .models import PaymentMethod
from .models import Product
from .models import Order
from .models import ProductOrder
from .serializers import CashControlSerializer, CategorySerializer
from .serializers import ProductSerializer
from .serializers import PaymentMethodSerializer
from .serializers import OrderSerializer
from .structures import SellStructure, cashControlStructure


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
@permission_classes([IsAuthenticated])
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


def summary_sales_calculate(date, user):
    orders = Order.objects.filter(created__date=date, author=user)
    total = sum(map(lambda order: order.total, orders))
    sales = len(orders)
    detail = []
    payment_methods = set([order.payment_method for order in orders])
    for payment_method in payment_methods:
        sales_by_payment_method = list(
            filter(lambda order: order.payment_method == payment_method, orders)
        )
        total_by_payment_method = sum(map(lambda order: order.total, orders))
        detail.append(
            {
                "key": payment_method.id,
                "payment_method": payment_method.name,
                "sales": len(sales_by_payment_method),
                "total": total_by_payment_method,
            }
        )
    return {
        "total": total,
        "date": date,
        "date_format": date.strftime("%b %d, %Y"),
        "sales": sales,
        "detail": detail,
    }


@api_view(["GET"])
@permission_classes([AllowAny])
def summary_sales_by_date(request, date):
    from django.utils import dateparse

    """
    Summary of sales, ACCESS ROL: ANONYMOUS
    Report of sales for a closing control
    """

    try:
        date = dateparse.parse_date(date)
        summary = summary_sales_calculate(date, request.user)
        return JsonResponse(
            summary,
            safe=False,
            status=200,
        )
    except Exception as e:
        return JsonResponse({"message": str(e)}, status=400)


@api_view(["GET"])
@permission_classes([AllowAny])
def summary_sales(request):
    from django.utils import dateparse

    """
    Summary of sales, ACCESS ROL: ANONYMOUS
    Report of sales for a closing control
    """

    try:
        summary = summary_sales_calculate(datetime.date.today(), request.user)
        return JsonResponse(
            summary,
            safe=False,
            status=200,
        )
    except Exception as e:
        return JsonResponse({"message": str(e)}, status=400)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def cash_control_today(request):
    """
    Cash Control, ACCESS ROL: ANONYMOUS
    Saving current cash control
    """

    try:

        observation = request.data.get("observation", "")
        summary = summary_sales_calculate(datetime.date.today(), request.user)
        summary = cashControlStructure(**summary).dict()
        cash_control = CashControl(
            total=summary["total"],
            date=datetime.date.today(),
            sales=summary["sales"],
            author=request.user,
            detail=json.dumps(summary["detail"]),
            observation=observation,
        )
        cash_control.save()
        return JsonResponse(
            CashControlSerializer(cash_control).data, safe=False, status=200
        )
    except Exception as e:
        return JsonResponse({"message": str(e)}, status=400)
