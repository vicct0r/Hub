from django.urls import path
from . import views


urlpatterns = [
    path('v1/', views.ClientListCreateAPIView.as_view()),
    path('v1/c/<slug:slug>/', views.CdRetrieveUpdateDestroy.as_view(), name='cd_detail_slug'),
    path('v1/c/<int:id>/', views.CdRetrieveUpdateDestroy.as_view(), name='cd_detail_id')
]