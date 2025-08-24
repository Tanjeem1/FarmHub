from django.urls import path
from .views import UserViewSet, FarmViewSet, CowViewSet, ActivityViewSet, MilkProductionViewSet, MilkReportView

urlpatterns = [
    path('users/', UserViewSet.as_view({'get': 'list', 'post': 'create'}), name='user-list'),
    path('users/<int:pk>/', UserViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='user-detail'),
    path('farms/', FarmViewSet.as_view({'get': 'list', 'post': 'create'}), name='farm-list'),
    path('farms/<int:pk>/', FarmViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='farm-detail'),
    path('cows/', CowViewSet.as_view({'get': 'list', 'post': 'create'}), name='cow-list'),
    path('cows/<int:pk>/', CowViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='cow-detail'),
    path('activities/', ActivityViewSet.as_view({'get': 'list', 'post': 'create'}), name='activity-list'),
    path('activities/<int:pk>/', ActivityViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='activity-detail'),
    path('milk-productions/', MilkProductionViewSet.as_view({'get': 'list', 'post': 'create'}), name='milk-production-list'),
    path('milk-productions/<int:pk>/', MilkProductionViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='milk-production-detail'),
    path('milk-reports/', MilkReportView.as_view({'get': 'list'}), name='milk-report'),
]