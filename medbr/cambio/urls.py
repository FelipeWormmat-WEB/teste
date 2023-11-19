from django.urls import path

from .views import MoedasViews

app_name = "cambio"


urlpatterns = [path("", MoedasViews.as_view(), name="index")]
