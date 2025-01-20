from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core.views import ContratoViewSet

router = DefaultRouter()
router.register(r'contratos', ContratoViewSet)

urlpatterns = [
    path('api/v1/', include(router.urls)),
]
