from django.urls import path
from .views import (
    # Country
    CountryListView, CountryDetailView, CountryCreateView, CountryUpdateView, CountryDeleteView,
    # Region
    RegionListView, RegionDetailView, RegionCreateView, RegionUpdateView, RegionDeleteView,
    # District
    DistrictListView, DistrictDetailView, DistrictCreateView, DistrictUpdateView, DistrictDeleteView,
    # Ward
    WardListView, WardDetailView, WardCreateView, WardUpdateView, WardDeleteView,
    # VillageStreet
    VillageStreetListView, VillageStreetDetailView, VillageStreetCreateView, VillageStreetUpdateView, VillageStreetDeleteView,
    # Hamlet
    HamletListView, HamletDetailView, HamletCreateView, HamletUpdateView, HamletDeleteView,
    # Site
    SiteListView, SiteDetailView, SiteCreateView, SiteUpdateView, SiteDeleteView,
)

app_name = 'locations'

urlpatterns = [
    # Country URLs
    path('countries/', CountryListView.as_view(), name='country-list'),
    path('countries/create/', CountryCreateView.as_view(), name='country-create'),
    path('countries/<int:pk>/', CountryDetailView.as_view(), name='country-detail'),
    path('countries/<int:pk>/edit/', CountryUpdateView.as_view(), name='country-edit'),
    path('countries/<int:pk>/delete/', CountryDeleteView.as_view(), name='country-delete'),

    # Region URLs
    path('regions/', RegionListView.as_view(), name='region-list'),
    path('regions/create/', RegionCreateView.as_view(), name='region-create'),
    path('regions/<int:pk>/', RegionDetailView.as_view(), name='region-detail'),
    path('regions/<int:pk>/edit/', RegionUpdateView.as_view(), name='region-edit'),
    path('regions/<int:pk>/delete/', RegionDeleteView.as_view(), name='region-delete'),

    # District URLs
    path('districts/', DistrictListView.as_view(), name='district-list'),
    path('districts/create/', DistrictCreateView.as_view(), name='district-create'),
    path('districts/<int:pk>/', DistrictDetailView.as_view(), name='district-detail'),
    path('districts/<int:pk>/edit/', DistrictUpdateView.as_view(), name='district-edit'),
    path('districts/<int:pk>/delete/', DistrictDeleteView.as_view(), name='district-delete'),

    # Ward URLs
    path('wards/', WardListView.as_view(), name='ward-list'),
    path('wards/create/', WardCreateView.as_view(), name='ward-create'),
    path('wards/<int:pk>/', WardDetailView.as_view(), name='ward-detail'),
    path('wards/<int:pk>/edit/', WardUpdateView.as_view(), name='ward-edit'),
    path('wards/<int:pk>/delete/', WardDeleteView.as_view(), name='ward-delete'),

    # VillageStreet URLs
    path('villages/', VillageStreetListView.as_view(), name='villagestreet-list'),
    path('villages/create/', VillageStreetCreateView.as_view(), name='villagestreet-create'),
    path('villages/<int:pk>/', VillageStreetDetailView.as_view(), name='villagestreet-detail'),
    path('villages/<int:pk>/edit/', VillageStreetUpdateView.as_view(), name='villagestreet-edit'),
    path('villages/<int:pk>/delete/', VillageStreetDeleteView.as_view(), name='villagestreet-delete'),

    # Hamlet URLs
    path('hamlets/', HamletListView.as_view(), name='hamlet-list'),
    path('hamlets/create/', HamletCreateView.as_view(), name='hamlet-create'),
    path('hamlets/<int:pk>/', HamletDetailView.as_view(), name='hamlet-detail'),
    path('hamlets/<int:pk>/edit/', HamletUpdateView.as_view(), name='hamlet-edit'),
    path('hamlets/<int:pk>/delete/', HamletDeleteView.as_view(), name='hamlet-delete'),

    # Site URLs
    path('sites/', SiteListView.as_view(), name='site-list'),
    path('sites/create/', SiteCreateView.as_view(), name='site-create'),
    path('sites/<int:pk>/', SiteDetailView.as_view(), name='site-detail'),
    path('sites/<int:pk>/edit/', SiteUpdateView.as_view(), name='site-edit'),
    path('sites/<int:pk>/delete/', SiteDeleteView.as_view(), name='site-delete'),
]
