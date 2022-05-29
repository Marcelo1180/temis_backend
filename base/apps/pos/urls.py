from base.apps.pos import views
from django.urls import path, re_path


urlpatterns = [
    path('categories/', views.CategoryListView.as_view()),
    path('products/', views.ProductListView.as_view()),
    path('payment_methods/', views.PaymentMethodListView.as_view()),
    path('order/', views.OrderCreateView.as_view()),
    path('sell/', views.sell_create),
    re_path(r'summary/sales/(?P<date>\d{4}-\d{2}-\d{2})/$', views.summary_sales_by_date),
    path('summary/sales/today/', views.summary_sales),
    path('cash/control/today/', views.cash_control_today),
]
