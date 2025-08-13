from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from urllib3 import request
from .models import Household
from .forms import HouseholdForm
from rest_framework import viewsets
from .serializers import HouseholdSerializer
import csv
from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import HouseholdUploadForm
from io import TextIOWrapper
from django.http import HttpResponse


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
    
    
    
import csv
from django.contrib import messages
from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import HttpResponse
from .models import Household


class HouseholdUploadView(View):
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
            # Skip completely empty rows
            if not any(row.values()):
                continue

            # Validation
            row_invalid = False
            try:
                men = int(row.get("number_of_men") or 0)
                women = int(row.get("number_of_women") or 0)
                phone = row.get("household_head_phone_number", "").strip()
                village = row.get("village_street", "").strip()
                head = row.get("household_head_name", "").strip()

                if not village or not head or not phone:
                    row_invalid = True
                    row['error'] = "Missing required fields."
                elif not phone.startswith("0") or len(phone) != 10:
                    row_invalid = True
                    row['error'] = "Phone must be 10 digits starting with 0."

            except Exception as e:
                row_invalid = True
                row['error'] = str(e)

            if row_invalid:
                invalid_rows.append(row)
            else:
                Household.objects.create(
                    household_head_name=head,
                    number_of_men=men,
                    number_of_women=women,
                    household_head_phone_number=phone,
                    village_street=village,
                    veo=veo_user
                )

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
            "village_street",
            "veo_username"
        ])

        # Example row
        writer.writerow(["John Doe", "2", "3", "0712345678", "Kijiji A", "veo1"])

        # Empty row then available usernames
        writer.writerow([])
        writer.writerow(["Available VEO Usernames"])
        for user in User.objects.all():
            writer.writerow([user.username])

        return response
    
    
# Download invalid rows as CSV
class DownloadInvalidRowsView(View):
    def post(self, request, *args, **kwargs):
        import json
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
