from django.urls import path
from . import views

urlpatterns = [
    path('', views.OrderListAPIView.as_view()),
    path('<uuid:id>/', views.OrderDetailView.as_view(), name='order_detail'),
    path('request/', views.OrderCreateAPIView.as_view()),
]