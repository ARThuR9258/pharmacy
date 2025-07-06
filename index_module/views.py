from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView, UpdateView, DeleteView

from index_module.forms import DrugForm
from index_module.models import Drugs


# Create your views here.


class DrugCreateView(LoginRequiredMixin,CreateView):
    model = Drugs
    fields = ['name' , 'number' , 'category' , 'expiration_date' , 'description' , 'date_in_warehouse']
    template_name = 'index_module/main_page.html'
    success_url = reverse_lazy('add_drug')

    def get_context_data(self, *args ,**kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'افزودن دارو جدید'
        return context


class SearchDrugView(LoginRequiredMixin,ListView):
    model = Drugs
    template_name = 'index_module/search_medicine.html'
    context_object_name = 'medicines'
    paginate_by = 5

    def get_queryset(self):
        query = self.request.GET.get('medicine_name' , '')

        objects = None
        if query:
            objects = Drugs.objects.filter(name__icontains=query)
        if not objects:
            objects = Drugs.objects.all()
        return objects


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('medicine_name', '')

        if context['search_query'] and len(self.get_queryset()) == Drugs.objects.count():
           context['is_empty'] = True

        return context


class EditDrugView(UpdateView):
    model = Drugs
    form_class = DrugForm
    template_name = 'index_module/edit_drug.html'
    success_url = reverse_lazy('search_drug')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class DeleteDrugView(DeleteView):
    model = Drugs
    template_name = 'index_module/delete_drug.html'
    success_url = reverse_lazy('search_drug')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class FirstPageView(View):
    def get(self,request):
        return render(request , 'index_module/first_page.html')
















