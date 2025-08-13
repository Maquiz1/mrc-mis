from django.urls import path
from .views import (
    CountryListView, CountryDetailView,
    CountryCreateView, CountryUpdateView, CountryDeleteView,
    RegionDetailView, DistrictDetailView, SiteDetailView
)

app_name = 'locations'

urlpatterns = [
    path('countries/', CountryListView.as_view(), name='country-list'),
    path('countries/create/', CountryCreateView.as_view(), name='country-create'),
    path('countries/<int:pk>/', CountryDetailView.as_view(), name='country-detail'),
    path('countries/<int:pk>/edit/', CountryUpdateView.as_view(), name='country-edit'),
    path('countries/<int:pk>/delete/', CountryDeleteView.as_view(), name='country-delete'),
    
    path('regions/<int:pk>/', RegionDetailView.as_view(), name='region-detail'),
    path('districts/<int:pk>/', DistrictDetailView.as_view(), name='district-detail'),
    path('sites/<int:pk>/', SiteDetailView.as_view(), name='site-detail'),
]
