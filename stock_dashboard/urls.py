from django.urls import path
from . import views

app_name = "stock_dashboard"

urlpatterns = [
    path("<str:ticker>/", views.display_ticker, name="display_ticker")
]