from django.urls import path
from . import views


urlpatterns = [
    path('request/', views.CdRequestAPIView.as_view(), name='cd_request'),
    path('cd/register/', views.CdRegisterAPIView.as_view(), name='cd_register'),
    path('cd/update/<slug:slug>/', views.CdPatchAPIView.as_view(), name='cd_edit'),
    path('cd/info/', views.CdListAPIView.as_view(), name='cd_info'),    
    path('cd/info/slug/<slug:slug>/', views.CdListAPIView.as_view(), name='cd_detail_slug'),
    path('cd/info/id/<int:pk>/', views.CdListAPIView.as_view(), name='cd_detail_id'),
]