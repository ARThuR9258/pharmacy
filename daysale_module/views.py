from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView, DeleteView, UpdateView

from daysale_module.forms import DailySaleForm
from daysale_module.models import DailySale
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.





class DailySaleCreateView(LoginRequiredMixin,CreateView):
    model = DailySale
    form_class = DailySaleForm
    template_name = 'daysale_module/submit_daily_sales.html'
    success_url = reverse_lazy('search_sale')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class SearchDailySaleView(LoginRequiredMixin,ListView):
    model = DailySale
    template_name = 'daysale_module/search_daily_sales.html'
    context_object_name = 'day_sales'
    paginate_by = 20


    def get_queryset(self):
        query = self.request.GET.get('date' , '')
        if query:
            objects = DailySale.objects.filter(date__icontains=query, user= self.request.user)
        else:
            objects = DailySale.objects.filter(user=self.request.user)
        return objects

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('date' , '')
        if context['search_query'] and len(self.get_queryset()) == 0:
            context['is_empty'] = True
        return context



class EditDrugView(LoginRequiredMixin, UpdateView):
    model = DailySale
    form_class = DailySaleForm
    template_name = 'daysale_module/edit_daily_sales.html'
    success_url = reverse_lazy('search_sale')

    def get_queryset(self):
        return DailySale.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context




class DeleteSaleView(LoginRequiredMixin, DeleteView):
    model = DailySale
    template_name = 'daysale_module/delete_daily_sales.html'
    success_url = reverse_lazy('search_sale')

    def get_queryset(self):
        return DailySale.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

