from base.apps.pos import views
from django.urls import path


urlpatterns = [
    path('categories/', views.CategoryListView.as_view()),
    path('products/', views.ProductListView.as_view()),
    path('payment_methods/', views.PaymentMethodListView.as_view()),
]
