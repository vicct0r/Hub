from django.urls import path
from . import views

urlpatterns = [
    path('', views.OrderListCreateAPIView.as_view()),
    path('<uuid:id>/', views.OrderRetrieveAPIView.as_view(), name='order_detail'),
    path('request/', views.OrderCreateAPIView.as_view()),
    path('o/<uuid:id>/', views.OrderRetrieveUpdateDeleteAPIView.as_view()),
]