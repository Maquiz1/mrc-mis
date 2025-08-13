from django.urls import path
from .views import DashboardHomeView,DashboardIndexView

app_name = "dashboard"

urlpatterns = [
    path("", DashboardHomeView.as_view(), name="dashboard"),
    path("index2/", DashboardIndexView.as_view(), name="index"),
]
