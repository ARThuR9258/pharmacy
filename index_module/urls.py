from re import search

from django.urls import path
from . import views

urlpatterns = [
    path('' , views.FirstPageView.as_view(),name = 'first_page'),
    path('add-drug' , views.DrugCreateView.as_view(),name = 'add_drug'),

    path('search-drug' , views.SearchDrugView.as_view() , name = 'search_drug'),
    path('edit-drug/<int:pk>' , views.EditDrugView.as_view() , name = 'edit_drug'),
    path('delete-drug/<int:pk>' , views.DeleteDrugView.as_view() , name = 'delete_drug'),
    path('expired-drugs' , views.ExpiredDrugsView.as_view() , name = 'expired-drugs'),
]