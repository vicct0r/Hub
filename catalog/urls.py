from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    path('', views.CatalogListCreateAPIView.as_view()),
    path('p/<slug:slug>/', views.CatalogRetrieveAPIView.as_view(), name='slug_detail'),
    path('<uuid:id>/', views.CatalogRetrieveUpdateDeleteAPIView.as_view(), name='product_detail'),
]