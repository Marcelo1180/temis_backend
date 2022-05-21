from base.apps.scale import views
from django.urls import path


urlpatterns = [
    path('weight/', views.scale_weight),
]
