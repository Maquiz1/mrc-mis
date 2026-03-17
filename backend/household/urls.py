from django.urls import path
from household.views import (
    HamletExpectationListView,
    HamletExpectationDetailView,
    HamletExpectationCreateView,
    HamletExpectationUpdateView,
    HamletExpectationDeleteView,
    HamletHouseholdExpectationUploadView,
    HamletHouseholdExpectationDownloadView,
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
    path('', HamletExpectationListView.as_view(), name='expectation-list'),
    path('<int:pk>/', HamletExpectationDetailView.as_view(), name='expectation-detail'),
    path('add/', HamletExpectationCreateView.as_view(), name='expectation-add'),
    path('<int:pk>/edit/', HamletExpectationUpdateView.as_view(), name='expectation-edit'),
    path('<int:pk>/delete/', HamletExpectationDeleteView.as_view(), name='expectation-delete'),
    path('upload/', HamletHouseholdExpectationUploadView.as_view(), name='expectation-upload'),
    path('download/', HamletHouseholdExpectationDownloadView.as_view(), name='expectation-download'),  # Download Excel/CSV template

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