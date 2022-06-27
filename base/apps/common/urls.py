from base.apps.common import views
from django.urls import path, re_path


urlpatterns = [
    path('categories/', views.CategoryListView.as_view()),
    path('products/', views.ProductListView.as_view()),
    path('payment_methods/', views.PaymentMethodListView.as_view()),
]
