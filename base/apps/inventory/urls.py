from base.apps.inventory import views
from django.urls import path, re_path


urlpatterns = [
    path('report/product_by_order', views.report_products_by_order),
]
