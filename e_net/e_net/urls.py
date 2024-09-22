from django.urls import path, include
from rest_framework.routers import DefaultRouter
from network.views import NetworkNodeViewSet, ProductViewSet, NetworkNodeDebtStatsViewSet, QRCodeViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.contrib import admin

router = DefaultRouter()
router.register(r'nodes', NetworkNodeViewSet)
router.register(r'products', ProductViewSet)
router.register(r'stats/debt', NetworkNodeDebtStatsViewSet, basename='debt-stats')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/generate_qr/', QRCodeViewSet.as_view({'get': 'generate_qr'}), name='generate_qr'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), 
]
