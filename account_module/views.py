import random

from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone

from datetime import timedelta
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.template.context_processors import request
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, UpdateView
from django.contrib import messages
from django import forms

from daysale_module.models import DailySale
from index_module.models import Drugs
from . import forms
from .forms import SignUpForm, PasswordResetForm, VerifyCodeForm, ResetPasswordForm, RegistrationVerifyCodeForm
from .models import User, PasswordResetCode


# Create your views here.

class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'account_module/sign_up.html'
    success_url = reverse_lazy('signup_verify_page')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs




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
    form_class = PasswordResetForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']
            try:
                user = User.objects.get(phone_number=phone_number)
                code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
                PasswordResetCode.objects.create(user=user, code=code)
                # messages.success(request, f"کد تأیید به شماره {phone_number} ارسال شد.")
                request.session['reset_phone'] = phone_number
                return redirect('verify_page')
            except User.DoesNotExist:
                form.add_error('phone_number', 'کاربری با این شماره موبایل وجود ندارد!')
        return render(request, self.template_name, {'form': form})


class VerifyCodeView(View):
    template_name = 'account_module/verify_code.html'
    form_class = VerifyCodeForm

    def get(self, request, *args, **kwargs):
        phone = request.session.get('reset_phone', '')
        form = self.form_class(phone_number=phone)
        return render(request, self.template_name, {'form': form, 'phone': phone})

    def post(self, request, *args, **kwargs):
        phone = request.session.get('reset_phone', '')
        form = self.form_class(phone_number=phone, data=request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            try:
                user = User.objects.get(phone_number=phone)
                reset_code = PasswordResetCode.objects.filter(user=user, code=code, is_used=False).first()
                if reset_code and reset_code.created_at:
                    reset_code.is_used = True
                    reset_code.save()
                    request.session['reset_user_id'] = user.id
                    return redirect('reset_password_page')
                else:
                    form.add_error('code', 'کد نامعتبر یا منقضی شده است.')
            except User.DoesNotExist:
                form.add_error('code', 'کاربر یافت نشد.')
        return render(request, self.template_name, {'form': form, 'phone': phone})



class ResetPasswordView(LoginRequiredMixin, View):
    template_name = 'account_module/reset_password.html'
    form_class = ResetPasswordForm
    login_url = '/login/'  # ریدایرکت به صفحه لاگین اگر کاربر لاگین نکرده باشه

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = request.user  # کاربر لاگین‌شده
            if user.is_authenticated:
                user.set_password(form.cleaned_data['new_password'])
                user.save()
                messages.success(request, "رمز عبور با موفقیت تغییر کرد.")
                return redirect('log_in_page')
            else:
                messages.error(request, "لطفاً ابتدا وارد حساب خود شوید.")
                return redirect(self.login_url)
        return render(request, self.template_name, {'form': form})




class SubscribeView(View):
    template_name = 'account_module/subscription.html'
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class SignUpVerifyCode(View):
    def get(self, request):
        phone_number = request.session.get('phone_number')
        if not phone_number:
            messages.error(request, 'لطفاً ابتدا فرم ثبت‌نام را پر کنید.')
            return redirect('sign_up_page')
        form = RegistrationVerifyCodeForm(phone_number=phone_number)
        return render(request, 'account_module/signup_verify_code.html', {'form': form})

    def post(self, request):
        phone_number = request.session.get('phone_number')
        if not phone_number:
            # messages.error(request, 'لطفاً ابتدا فرم ثبت‌نام را پر کنید.')
            return redirect('sign_up_page')

        form = RegistrationVerifyCodeForm(phone_number=phone_number, data=request.POST)
        if form.is_valid():
            user = User.objects.get(phone_number=phone_number)
            reset_code = PasswordResetCode.objects.get(user=user, code=form.cleaned_data['code'], is_used=False)
            reset_code.is_used = True
            reset_code.save()
            user.is_verified = True  # تأیید کاربر
            user.save()
            login(request, user)  # ورود خودکار کاربر
            # messages.success(request, 'ثبت‌نام با موفقیت انجام شد!')
            del request.session['phone_number']  # پاک کردن سشن
            return redirect('first_page')  # به صفحه اصلی برو
        else:
            # messages.error(request, 'کد تأیید اشتباه است!')
            return render(request, 'account_module/signup_verify_code.html', {'form': form})



class UserPanelView(LoginRequiredMixin,View):
    template_name = 'account_module/user_panel.html'

    def get_queryset(self):
        today = timezone.now().date()
        six_month_later = today + timedelta(days=180)
        return Drugs.objects.filter(user=self.request.user,expiration_date__lte=six_month_later)

    def get(self,request,*args,**kwargs):
        context={
        'medicine_count':Drugs.objects.filter(user=self.request.user).count(),
        'expiring_soon': self.get_queryset().count(),
        'day_sales_count': DailySale.objects.filter(user=self.request.user).count(),
        }
        return render(request ,self.template_name,context)


