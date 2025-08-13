from django.urls import path
from .views import (
    HouseholdCreateView,
    HouseholdListView,
    HouseholdDetailView,
    HouseholdUpdateView,
    HouseholdDeleteView
)
app_name = 'household'

urlpatterns = [
    path('household/create-household/', HouseholdCreateView.as_view(), name='create-household'),
    path('household/household-list/', HouseholdListView.as_view(), name='household-list'),
    path('household/household-detail/<int:pk>/', HouseholdDetailView.as_view(), name='household-detail'),
    path('household/household-edit/<int:pk>/', HouseholdUpdateView.as_view(), name='household-edit'),
    path('household/household-delete/<int:pk>/', HouseholdDeleteView.as_view(), name='household-delete'),
]