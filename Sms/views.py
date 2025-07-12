from django.shortcuts import render
from django.views.generic import CreateView, TemplateView
from django.contrib.auth import get_user_model

from ACL.mixins import PermissionMixin
from Class.models import Class

User = get_user_model()


class SmsGroupSendView(PermissionMixin, TemplateView):
    permissions = ['sms_send']
    template_name = "sms/admin/sms/form.html"

    def get_context_data(self, **kwargs):
        context = {
            'object_list': User.objects.all(),
            'classes': Class.objects.all(),
        }

        return context
