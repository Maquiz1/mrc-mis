import csv
import math
import tempfile
import json
from io import TextIOWrapper
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView, View, FormView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse
from rest_framework import viewsets

from ..models import Household,HamletHouseholdExpectation
from ..forms import HouseholdForm,HamletHouseholdExpectationForm,HamletHouseholdExpectationUploadForm
from ..serializers import HouseholdSerializer
from locations.models import Region, District, Ward, VillageStreet, Hamlet


# List all expectations
class HamletExpectationListView(ListView):
    model = HamletHouseholdExpectation
    template_name = 'expectations/expectation_list.html'
    context_object_name = 'expectations'

# Detail of one expectation
class HamletExpectationDetailView(DetailView):
    model = HamletHouseholdExpectation
    template_name = 'expectations/expectation_detail.html'
    context_object_name = 'expectation'

# Create new expectation
class HamletExpectationCreateView(CreateView):
    model = HamletHouseholdExpectation
    form_class = HamletHouseholdExpectationForm
    template_name = 'expectations/expectation_form.html'

    def get_success_url(self):
        # Redirect to hamlet detail page
        return reverse_lazy('household:expectation-list')

# Update expectation
class HamletExpectationUpdateView(UpdateView):
    model = HamletHouseholdExpectation
    form_class = HamletHouseholdExpectationForm
    template_name = 'expectations/expectation_form.html'

    def get_success_url(self):
        return reverse_lazy('household:expectation-list')

# Delete expectation
class HamletExpectationDeleteView(DeleteView):
    model = HamletHouseholdExpectation
    template_name = 'expectations/expectation_confirm_delete.html'
    success_url = reverse_lazy('household:expectation-list')

class HamletHouseholdExpectationListView(ListView):
    model = HamletHouseholdExpectation
    template_name = 'expectations/expectation_list.html'
    context_object_name = 'expectations'

class HamletHouseholdExpectationUploadView(FormView):
    template_name = 'expectations/expectation_upload.html'
    form_class = HamletHouseholdExpectationUploadForm

    def form_valid(self, form):
        form.save()
        return redirect('household:expectation-list')

class HamletHouseholdExpectationDownloadView(View):
    def get(self, request, *args, **kwargs):
        # Create the HTTP response with CSV content
        response = HttpResponse(
            content_type='text/csv',
            headers={'Content-Disposition': 'attachment; filename="hamlet_household_expectations_template.csv"'},
        )

        writer = csv.writer(response)
        # Write header row
        writer.writerow(['hamlet', 'expected_households'])

        # Optional: If you want to include existing expectations from DB
        # from .models import HamletHouseholdExpectation
        # for item in HamletHouseholdExpectation.objects.all():
        #     writer.writerow([item.hamlet.name, item.expected_households])

        return response
    
class HouseholdListView(LoginRequiredMixin, ListView):
    model = Household
    template_name = 'household/household_list.html'
    context_object_name = 'households'


class HouseholdCreateView(LoginRequiredMixin, CreateView):
    model = Household
    form_class = HouseholdForm
    template_name = 'household/household_form.html'
    success_url = reverse_lazy('household:household-list')

    def form_valid(self, form):
        form.instance.veo = self.request.user
        return super().form_valid(form)


class HouseholdDetailView(LoginRequiredMixin, DetailView):
    model = Household
    template_name = 'household/household_detail.html'
    context_object_name = 'household'


class HouseholdUpdateView(LoginRequiredMixin, UpdateView):
    model = Household
    form_class = HouseholdForm
    template_name = 'household/household_form.html'
    success_url = reverse_lazy('household:household-list')


class HouseholdDeleteView(LoginRequiredMixin, DeleteView):
    model = Household
    template_name = 'household/household_confirm_delete.html'
    success_url = reverse_lazy('household:household-list')


class HouseholdViewSet(viewsets.ModelViewSet):
    queryset = Household.objects.all()
    serializer_class = HouseholdSerializer


class HouseholdUploadView(LoginRequiredMixin, ListView):
    template_name = "household/upload.html"

    def get(self, request, *args, **kwargs):
        veo_users = User.objects.all()
        return render(request, self.template_name, {"veo_users": veo_users})

    def post(self, request, *args, **kwargs):
        veo_users = User.objects.all()
        invalid_rows = []

        veo_id = request.POST.get("veo")
        try:
            veo_user = User.objects.get(id=veo_id)
        except User.DoesNotExist:
            messages.error(request, "Selected VEO does not exist.")
            return redirect("household:upload-households")

        file = request.FILES.get("file")
        if not file or not file.name.endswith(".csv"):
            messages.error(request, "Please upload a CSV file.")
            return redirect("household:upload-households")

        csv_file = TextIOWrapper(file.file, encoding="utf-8")
        reader = csv.DictReader(csv_file)

        for idx, row in enumerate(reader, start=1):
            if not any(row.values()):
                continue

            row_invalid = False
            try:
                head = row.get("household_head_name", "").strip()
                men = int(row.get("number_of_men") or 0)
                women = int(row.get("number_of_women") or 0)
                phone = row.get("household_head_phone_number", "").strip()

                region_name = row.get("region", "").strip()
                district_name = row.get("district", "").strip()
                ward_name = row.get("ward", "").strip()
                village_name = row.get("village", "").strip()
                hamlet_name = row.get("hamlet", "").strip()

                # Validate required fields
                if not all([head, phone, region_name, district_name, ward_name, village_name, hamlet_name]):
                    row_invalid = True
                    row["error"] = "Missing required fields."
                elif not phone.startswith("0") or len(phone) != 10:
                    row_invalid = True
                    row["error"] = "Phone must be 10 digits starting with 0."

                # Lookup location objects
                if not row_invalid:
                    try:
                        region = Region.objects.get(name__iexact=region_name)
                        district = District.objects.get(name__iexact=district_name, region=region)
                        ward = Ward.objects.get(name__iexact=ward_name, district=district)
                        village = VillageStreet.objects.get(name__iexact=village_name, ward=ward)
                        hamlet = Hamlet.objects.get(name__iexact=hamlet_name, village=village)
                    except Region.DoesNotExist:
                        row_invalid = True
                        row["error"] = f"Region '{region_name}' not found."
                    except District.DoesNotExist:
                        row_invalid = True
                        row["error"] = f"District '{district_name}' not found in region '{region_name}'."
                    except Ward.DoesNotExist:
                        row_invalid = True
                        row["error"] = f"Ward '{ward_name}' not found in district '{district_name}'."
                    except VillageStreet.DoesNotExist:
                        row_invalid = True
                        row["error"] = f"Village '{village_name}' not found in ward '{ward_name}'."
                    except Hamlet.DoesNotExist:
                        row_invalid = True
                        row["error"] = f"Hamlet '{hamlet_name}' not found in village '{village_name}'."

                if row_invalid:
                    invalid_rows.append(row)
                else:
                    Household.objects.create(
                        household_head_name=head,
                        number_of_men=men,
                        number_of_women=women,
                        household_head_phone_number=phone,
                        region=region,
                        district=district,
                        ward=ward,
                        village=village,
                        hamlet=hamlet,
                        veo=veo_user
                    )

            except Exception as e:
                row["error"] = str(e)
                invalid_rows.append(row)

        if invalid_rows:
            messages.warning(request, f"{len(invalid_rows)} rows were invalid and not uploaded.")
        else:
            messages.success(request, "All households uploaded successfully.")

        return render(request, self.template_name, {
            "veo_users": veo_users,
            "invalid_rows": invalid_rows
        })


class HouseholdTemplateDownloadView(View):
    def get(self, request):
        response = HttpResponse(content_type="text/csv")
        response['Content-Disposition'] = 'attachment; filename="household_template.csv"'
        writer = csv.writer(response)

        # CSV header
        writer.writerow([
            "household_head_name",
            "number_of_men",
            "number_of_women",
            "household_head_phone_number",
            "region",
            "district",
            "ward",
            "village",
            "hamlet",
            "veo_username"
        ])

        # Example row
        writer.writerow(["John Doe", "2", "3", "0712345678", "Dodoma", "Dodoma Urban", "Kizota", "Kijiji A", "Kitongoji B", "veo1"])

        # Empty row then available usernames
        writer.writerow([])
        writer.writerow(["Available VEO Usernames"])
        for user in User.objects.all():
            writer.writerow([user.username])

        return response


class DownloadInvalidRowsView(View):
    def post(self, request, *args, **kwargs):
        invalid_rows_json = request.POST.get("invalid_rows")
        fieldnames = request.POST.get("fieldnames")
        if not invalid_rows_json or not fieldnames:
            messages.error(request, "No invalid rows to download.")
            return redirect("household:household-upload")

        invalid_rows = json.loads(invalid_rows_json)
        fieldnames = json.loads(fieldnames)

        temp_file = tempfile.NamedTemporaryFile(mode="w+", delete=False, newline="", suffix=".csv")
        writer = csv.DictWriter(temp_file, fieldnames=fieldnames + ["error"])
        writer.writeheader()
        for row in invalid_rows:
            writer.writerow(row)
        temp_file.close()

        response = HttpResponse(open(temp_file.name, "r"), content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="invalid_households.csv"'
        return response
