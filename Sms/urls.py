from django.urls import path
from .views import *

urlpatterns = []

dashboard_urls = [
    path('dashboard/sms/group/send/', SmsGroupSendView.as_view(), name='sms-group-send'),
]

urlpatterns += dashboard_urls
