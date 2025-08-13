from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Household
from .forms import HouseholdForm

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
