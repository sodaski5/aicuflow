from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NodeViewSet, predict

router = DefaultRouter()
router.register(r'nodes', NodeViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('predict/', predict),
]