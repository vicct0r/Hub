from django.urls import path
from . import views

urlpatterns = [
    path('request/', views.CdRequestAPIView.as_view(), name='cd_request'),
    path('cd/', views.CdListCreateAPIView.as_view(), name='cd_list_create'),
    path('cd/<int:id>/', views.CdRetrieveUpdateDestroy.as_view(), name='cd_detail_id'),
    path('cd/<slug:slug>/', views.CdRetrieveUpdateDestroy.as_view(), name='cd_detail_slug'),
]