from django.urls import path
from cambio.views import ExchangeRatesView
app_name = "cambio"

urlpatterns = [
    path("", ExchangeRatesView.as_view(), name="index"),
    ]
