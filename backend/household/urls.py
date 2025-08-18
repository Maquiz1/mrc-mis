from django.urls import path
from . import views
from .views import (
    HouseholdCreateView,
    HouseholdListView,
    HouseholdDetailView,
    HouseholdUpdateView,
    HouseholdDeleteView,
    HouseholdUploadView,
    HouseholdTemplateDownloadView,
    DownloadInvalidRowsView
)

app_name = 'household'

urlpatterns = [
    path('', views.HamletExpectationListView.as_view(), name='expectation-list'),
    path('<int:pk>/', views.HamletExpectationDetailView.as_view(), name='expectation-detail'),
    path('add/', views.HamletExpectationCreateView.as_view(), name='expectation-add'),
    path('<int:pk>/edit/', views.HamletExpectationUpdateView.as_view(), name='expectation-edit'),
    path('<int:pk>/delete/', views.HamletExpectationDeleteView.as_view(), name='expectation-delete'),
    path('upload/', views.HamletHouseholdExpectationUploadView.as_view(), name='expectation-upload'),
    path('download/', views.HamletHouseholdExpectationDownloadView.as_view(), name='expectation-download'),  # Download Excel/CSV template

    path('household/create-household/', HouseholdCreateView.as_view(), name='create-household'),
    path('household/household-list/', HouseholdListView.as_view(), name='household-list'),
    path('household/household-detail/<int:pk>/', HouseholdDetailView.as_view(), name='household-detail'),
    path('household/household-edit/<int:pk>/', HouseholdUpdateView.as_view(), name='household-edit'),
    path('household/household-delete/<int:pk>/', HouseholdDeleteView.as_view(), name='household-delete'),
    path("upload/", HouseholdUploadView.as_view(), name="household-upload"),
    path("template/download/", HouseholdTemplateDownloadView.as_view(), name="household-template-download"),
    path('household/download-invalid/', DownloadInvalidRowsView.as_view(), name='download-invalid-rows'),
]


# from rest_framework import routers
# from .views import HouseholdViewSet

# router = routers.DefaultRouter()
# router.register(r'households', HouseholdViewSet)

# urlpatterns += router.urls