from django.urls import path
from . import views


urlpatterns = [
    path('submit-sale', views.DailySaleCreateView.as_view(), name= 'submit_day_sale'),
    path('search-sale', views.SearchDailySaleView.as_view(), name= 'search_sale')
]