from django.conf import settings
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter

from warehouse.users.api.views import UserViewSet, SupplierViewSet

router = DefaultRouter() if settings.DEBUG else SimpleRouter()

router.register("users", UserViewSet, basename="user")
router.register("supplier", SupplierViewSet)


app_name = "users"
urlpatterns = [
    path("", include(router.urls)),

]
