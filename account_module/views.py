import random
from time import timezone

from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.template.context_processors import request
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, UpdateView
from pyexpat.errors import messages
from django import forms

from . import forms
from .forms import SignUpForm
from .models import User, PasswordResetCode


# Create your views here.

class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'account_module/sign_up.html'
    success_url = reverse_lazy('log_in_page')



class LogInView(LoginView):
    template_name = 'account_module/log_in.html'
    redirect_authenticated_user = True
    success_url = reverse_lazy('first_page')

    # def form_valid(self, form):
    #     messages.success(self.request)
    #     return super().form_valid(form)
    #
    #
    # def form_invalid(self, form):
    #     messages.error(self,request)
    #     return super().form_invalid(form)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context






class ForgotPasswordView(View):
    template_name = 'account_module/forgot_password.html'


    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        phone = request.POST.get('phone')
        try:
            user = User.objects.get(phone_number=phone)
            code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
            PasswordResetCode.objects.create(user=user, code=code)
            # messages.success(request, f"کد تأیید به شماره {phone} ارسال شد.")
            request.session['reset_phone'] = phone
            return redirect('verify_page')
        except User.DoesNotExist:
             return render(request, self.template_name)


class VerifyCodeView(View):
    template_name = 'account_module/verify_code.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'phone': request.session.get('reset_phone', '')})

    def post(self, request, *args, **kwargs):
        code = request.POST.get('code')
        phone = request.session.get('reset_phone')
        try:
            user = User.objects.get(phone_number=phone)
            reset_code = PasswordResetCode.objects.filter(user=user, code=code, is_used=False).first()
            if reset_code and reset_code.created_at:
                reset_code.is_used = True
                reset_code.save()
                request.session['reset_user_id'] = user.id
                return redirect('reset_password_page')
            else:
                messages.error(request, "کد نامعتبر یا منقضی شده است.")
        except User.DoesNotExist:
            return render(request, self.template_name, {'phone': phone})



class ResetPasswordView(View):
    template_name = 'account_module/reset_password.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        user_id = request.session.get('reset_user_id')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        if new_password == confirm_password:
            try:
                user = User.objects.get(id=user_id)
                user.set_password(new_password)
                user.save()
                del request.session['reset_user_id']
                del request.session['reset_phone']
                messages.success(request, "رمز عبور با موفقیت تغییر کرد.")
                return redirect('sign_in')
            except User.DoesNotExist:
                messages.error(request, "خطا در ذخیره رمز.")
        else:
            messages.error(request, "رمزها مطابقت ندارند.")
        return render(request, self.template_name)










