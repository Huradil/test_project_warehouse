from django.conf import settings
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter

from warehouse.core.views import ProductViewSet, OrderViewSet

router = DefaultRouter() if settings.DEBUG else SimpleRouter()

router.register("products", ProductViewSet, basename="product")
router.register("orders", OrderViewSet, basename="order")


app_name = "core"
urlpatterns = [
    path("", include(router.urls)),

]
