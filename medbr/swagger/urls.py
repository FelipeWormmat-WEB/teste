from django.urls import path

from .views import CambiosListAPIView

app_name = "swagger"

urlpatterns = [
    path("cambio/", CambiosListAPIView.as_view(), name="list-api"),
]
