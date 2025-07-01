from django.urls import path, include
from .views import (
    BloodRequestDeleteView,
    BloodRequestListCreateView,
    BloodRequestStats,
    BloodRequestMarkFulfilled,
    BloodRequestRetrieveView,  # ✅ Add this
)
from rest_framework.routers import DefaultRouter
from .views import DonorViewSet

router = DefaultRouter()
router.register(r'donors', DonorViewSet, basename='donor')

urlpatterns = [
    path('requests/', BloodRequestListCreateView.as_view(), name='blood-request-list'),
    path('requests/<int:pk>/', BloodRequestRetrieveView.as_view(), name='blood-request-detail'),  # ✅ FIX
    path('requests/<int:pk>/delete/', BloodRequestDeleteView.as_view(), name='blood-request-delete'),
    path('requests/stats/', BloodRequestStats.as_view(), name='blood-request-stats'),
    path('requests/<int:pk>/donated/', BloodRequestMarkFulfilled.as_view(), name='blood-request-donated'),

    path('', include(router.urls)),
]
