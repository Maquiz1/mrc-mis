from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy,reverse
from .models import Country, Region, District, Site, Ward, VillageStreet, Hamlet
from .forms import CountryForm, RegionForm, DistrictForm, SiteForm, WardForm, VillageStreetForm, HamletForm
from django.shortcuts import get_object_or_404
from django import forms

# ------------------ Country ------------------
class CountryListView(ListView):
    model = Country
    template_name = 'locations/country_list.html'
    context_object_name = 'countries'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for country in context['countries']:
            country.district_count = sum([r.district_set.count() for r in country.region_set.all()])
            country.site_count = sum([d.site_set.count() for r in country.region_set.all() for d in r.district_set.all()])
        return context


class CountryDetailView(DetailView):
    model = Country
    template_name = 'locations/country_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        regions = Region.objects.filter(country=self.object)
        for region in regions:
            region.district_count = region.district_set.count()
            region.site_count = sum(d.site_set.count() for d in region.district_set.all())
        context['regions'] = regions
        return context

class CountryCreateView(CreateView):
    model = Country
    form_class = CountryForm
    template_name = 'locations/country_form.html'
    success_url = reverse_lazy('locations:country-list')

class CountryUpdateView(UpdateView):
    model = Country
    form_class = CountryForm
    template_name = 'locations/country_form.html'
    success_url = reverse_lazy('locations:country-list')

class CountryDeleteView(DeleteView):
    model = Country
    template_name = 'locations/country_confirm_delete.html'
    success_url = reverse_lazy('locations:country-list')


# ------------------ Region ------------------
class RegionListView(ListView):
    model = Region
    template_name = 'locations/region_list.html'

class RegionDetailView(DetailView):
    model = Region
    template_name = 'locations/region_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['districts'] = District.objects.filter(region=self.object)
        return context

class RegionCreateView(CreateView):
    model = Region
    fields = ['name', 'country']
    template_name = 'locations/region_form.html'

    def get_initial(self):
        initial = super().get_initial()
        country_id = self.request.GET.get('country')
        if country_id:
            country = get_object_or_404(Country, id=country_id)
            initial['country'] = country
        return initial

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if 'country' in self.request.GET:
            form.fields['country'].widget = forms.HiddenInput()
        return form

    def get_success_url(self):
        country_id = self.request.GET.get('country')
        if country_id:
            return reverse('locations:country-detail', args=[country_id])
        return reverse_lazy('locations:region-list')

class RegionUpdateView(UpdateView):
    model = Region
    form_class = RegionForm
    template_name = 'locations/region_form.html'
    success_url = reverse_lazy('locations:region-list')
    
    def get_success_url(self):
        if self.object.country:
            return reverse('locations:country-detail', args=[self.object.country.id])
        return reverse('locations:region-list')

class RegionDeleteView(DeleteView):
    model = Region
    template_name = 'locations/region_confirm_delete.html'
    success_url = reverse_lazy('locations:region-list')


# ------------------ District ------------------
class DistrictListView(ListView):
    model = District
    template_name = 'locations/district_list.html'

class DistrictDetailView(DetailView):
    model = District
    template_name = 'locations/district_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['wards'] = Ward.objects.filter(district=self.object)
        context['sites'] = Site.objects.filter(district=self.object)
        return context

class DistrictCreateView(CreateView):
    model = District
    form_class = DistrictForm
    template_name = 'locations/district_form.html'
    success_url = reverse_lazy('locations:district-list')
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if 'region' in self.request.GET:
            form.fields['region'].initial = self.request.GET.get('region')
            form.fields['region'].widget = forms.HiddenInput()
        return form
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if 'region' in self.request.GET:
            form.fields['region'].widget = forms.HiddenInput()
        return form

    def get_success_url(self):
        if self.object.region:
            return reverse('locations:region-detail', args=[self.object.region.id])
        return reverse('locations:district-list')

class DistrictUpdateView(UpdateView):
    model = District
    form_class = DistrictForm
    template_name = 'locations/district_form.html'
    success_url = reverse_lazy('locations:district-list')
    
    def get_success_url(self):
        if self.object.region:
            return reverse('locations:region-detail', args=[self.object.region.id])
        return reverse('locations:district-list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['wards'] = Ward.objects.filter(district=self.object)
        context['sites'] = Site.objects.filter(district=self.object)
        
        # Ensure region and country exist
        context['region'] = self.object.region if self.object.region else None
        context['country'] = self.object.region.country if self.object.region and self.object.region.country else None
        
        return context

class DistrictDeleteView(DeleteView):
    model = District
    template_name = 'locations/district_confirm_delete.html'
    success_url = reverse_lazy('locations:district-list')


# ------------------ Ward ------------------
class WardListView(ListView):
    model = Ward
    template_name = 'locations/ward_list.html'

class WardDetailView(DetailView):
    model = Ward
    template_name = 'locations/ward_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['villages'] = VillageStreet.objects.filter(ward=self.object)
        return context

class WardCreateView(CreateView):
    model = Ward
    form_class = WardForm
    template_name = 'locations/ward_form.html'
    success_url = reverse_lazy('locations:ward-list')
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if 'district' in self.request.GET:
            form.fields['district'].widget = forms.HiddenInput()
        return form

    def get_success_url(self):
        if self.object.district:
            return reverse('locations:district-detail', args=[self.object.district.id])
        return reverse('locations:ward-list')

class WardUpdateView(UpdateView):
    model = Ward
    form_class = WardForm
    template_name = 'locations/ward_form.html'
    success_url = reverse_lazy('locations:ward-list')
    
    def get_success_url(self):
        if self.object.district:
            return reverse('locations:district-detail', args=[self.object.district.id])
        return reverse('locations:ward-list')

class WardDeleteView(DeleteView):
    model = Ward
    template_name = 'locations/ward_confirm_delete.html'
    success_url = reverse_lazy('locations:ward-list')


# ------------------ VillageStreet ------------------
class VillageStreetListView(ListView):
    model = VillageStreet
    template_name = 'locations/villagestreet_list.html'

class VillageStreetDetailView(DetailView):
    model = VillageStreet
    template_name = 'locations/villagestreet_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hamlets'] = Hamlet.objects.filter(village=self.object)
        return context

class VillageStreetCreateView(CreateView):
    model = VillageStreet
    form_class = VillageStreetForm
    template_name = 'locations/villagestreet_form.html'
    success_url = reverse_lazy('locations:villagestreet-list')
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if 'ward' in self.request.GET:
            form.fields['ward'].widget = forms.HiddenInput()
        return form

    def get_success_url(self):
        if self.object.ward:
            return reverse('locations:ward-detail', args=[self.object.ward.id])
        return reverse('locations:villagestreet-list')

class VillageStreetUpdateView(UpdateView):
    model = VillageStreet
    form_class = VillageStreetForm
    template_name = 'locations/villagestreet_form.html'
    success_url = reverse_lazy('locations:villagestreet-list')
    
    def get_success_url(self):
        if self.object.ward:
            return reverse('locations:ward-detail', args=[self.object.ward.id])
        return reverse('locations:villagestreet-list')

class VillageStreetDeleteView(DeleteView):
    model = VillageStreet
    template_name = 'locations/villagestreet_confirm_delete.html'
    success_url = reverse_lazy('locations:villagestreet-list')


# ------------------ Hamlet ------------------
class HamletListView(ListView):
    model = Hamlet
    template_name = 'locations/hamlet_list.html'

class HamletDetailView(DetailView):
    model = Hamlet
    template_name = 'locations/hamlet_detail.html'

class HamletCreateView(CreateView):
    model = Hamlet
    form_class = HamletForm
    template_name = 'locations/hamlet_form.html'
    success_url = reverse_lazy('locations:hamlet-list')
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if 'village' in self.request.GET:
            form.fields['village'].widget = forms.HiddenInput()
        return form

    def get_success_url(self):
        if self.object.village:
            return reverse('locations:villagestreet-detail', args=[self.object.village.id])
        return reverse('locations:hamlet-list')

class HamletUpdateView(UpdateView):
    model = Hamlet
    form_class = HamletForm
    template_name = 'locations/hamlet_form.html'
    success_url = reverse_lazy('locations:hamlet-list')

class HamletDeleteView(DeleteView):
    model = Hamlet
    template_name = 'locations/hamlet_confirm_delete.html'
    success_url = reverse_lazy('locations:hamlet-list')


# ------------------ Site ------------------
class SiteListView(ListView):
    model = Site
    template_name = 'locations/site_list.html'

class SiteDetailView(DetailView):
    model = Site
    template_name = 'locations/site_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        district = self.object.district
        region = district.region
        country = region.country
        context.update({
            'district': district,
            'region': region,
            'country': country
        })
        return context

class SiteCreateView(CreateView):
    model = Site
    form_class = SiteForm
    template_name = 'locations/site_form.html'
    success_url = reverse_lazy('locations:site-list')
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if 'district' in self.request.GET:
            form.fields['district'].widget = forms.HiddenInput()
        return form

    def get_success_url(self):
        if self.object.district:
            return reverse('locations:district-detail', args=[self.object.district.id])
        return reverse('locations:site-list')

class SiteUpdateView(UpdateView):
    model = Site
    form_class = SiteForm
    template_name = 'locations/site_form.html'
    success_url = reverse_lazy('locations:site-list')

class SiteDeleteView(DeleteView):
    model = Site
    template_name = 'locations/site_confirm_delete.html'
    success_url = reverse_lazy('locations:site-list')
