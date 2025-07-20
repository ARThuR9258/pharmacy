from datetime import timezone, timedelta

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, View

from .forms import DrugForm
from .models import Drugs

class DrugCreateView(LoginRequiredMixin, CreateView):
    model = Drugs
    form_class = DrugForm
    template_name = 'index_module/main_page.html'
    success_url = reverse_lazy('search_drug')  # تغییر به صفحه جستجو

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'افزودن دارو جدید'
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class SearchDrugView(LoginRequiredMixin, ListView):
    model = Drugs
    template_name = 'index_module/search_medicine.html'
    context_object_name = 'medicines'
    paginate_by = 5

    def get_queryset(self):
        query = self.request.GET.get('medicine_name', '')
        if query:
            objects = Drugs.objects.filter(name__icontains=query, user=self.request.user)
        else:
            objects = Drugs.objects.filter(user=self.request.user)
        return objects

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('medicine_name', '')
        if context['search_query'] and len(self.get_queryset()) == 0:
            context['is_empty'] = True
        return context


class EditDrugView(LoginRequiredMixin, UpdateView):
    model = Drugs
    form_class = DrugForm
    template_name = 'index_module/edit_drug.html'
    success_url = reverse_lazy('search_drug')

    def get_queryset(self):
        return Drugs.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class DeleteDrugView(LoginRequiredMixin, DeleteView):
    model = Drugs
    template_name = 'index_module/delete_drug.html'
    success_url = reverse_lazy('search_drug')

    def get_queryset(self):
        return Drugs.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context



class ExpiredDrugsView(LoginRequiredMixin,ListView):
    model = Drugs
    template_name = 'index_module/expired_drugs.html'
    context_object_name = 'expired_medicines'
    paginate_by = 5

    def get_queryset(self):
        today = timezone.now().date()
        six_month_later = today + timedelta(days=180)
        return Drugs.objects.filter(user=self.request.user,expiration_date__lte=six_month_later)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['six_month_later'] = timezone.now().date() + timedelta(days=180)
        return context


class FirstPageView(View):
    def get(self, request):
        return render(request, 'index_module/first_page.html')