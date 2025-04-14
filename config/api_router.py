from django.urls import include, path


app_name = "api"
urlpatterns = [
    path("users/", include("warehouse.users.api.api_router")),
    path("core/", include("warehouse.core.api_router"))

]
