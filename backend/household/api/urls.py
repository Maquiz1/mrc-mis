from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    path('households/', views.HouseholdListCreateAPIView.as_view(), name='household-list-create'),
    path('households/<int:pk>/', views.HouseholdRetrieveUpdateAPIView.as_view(), name='household-detail'),
]
