import random
import re

from django import forms
from django.core import validators
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

from Sms.helpers import send_sms
from Sms.sms_texts import SMS_TEXTS
from .models import User, PasswordResetCode

mobile_regex = RegexValidator(
    regex=r'(^\+?(09|98|0)?(9([0-9]{9}))$)',
    message="شماره موبایل معتبر نیست."
)


class SignUpForm(forms.ModelForm):
    password = forms.CharField(min_length=8, max_length=100, required=True,
                                widget=forms.PasswordInput(attrs={'placeholder': 'رمز عبور'}),
                                label='رمز عبور')
    password2 = forms.CharField(min_length=8 ,max_length=100, required=True, widget=forms.PasswordInput(attrs={'placeholder': 'تکرار رمز عبور'}), label='تکرار رمز عبور')
    phone_number = forms.CharField(
        min_length=11 ,
        max_length=11,
        label= 'شاره موبایل' ,
        widget=forms.TextInput(attrs={'placeholder': 'مثال: 09123456789'}),
        validators=[mobile_regex]
    )


    class Meta:
        model = User
        fields = ['username', 'phone_number', 'password' , 'password2']
        widgets = {
            'username': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'نام کاربری',
            'error_message': 'نام کاربری وارد شده معتبر نیست'
            }),

            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'شماره موبایل',
                'error_message': 'شماره موبایل وارد شده معتبر نیست',
            }),

            'password': forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'کلمه عبور',
                'error_message': 'کلمه عبور وارد شده معتبر نیست'
            }),

            'password2': forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'تکرار کلمه عبور',
                'error_message': 'کلمه عبور مطابقت ندارد'
            }),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super().__init__(*args, **kwargs)
        if 'password' in self.fields:
            self.fields['password'].widget = forms.PasswordInput(attrs=self.fields['password'].widget.attrs)

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if User.objects.filter(phone_number=phone_number).exists():
            raise forms.ValidationError('این شماره موبایل قبلاً ثبت شده است!')
        return phone_number

    def clean_password2(self):
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password and password2 and password != password2:
            raise forms.ValidationError('رمز عبور با تکرار آن مغایرت دارد!')
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)
        if commit:
            user.save()
        verification_code = str(random.randint(100000, 999999))
        PasswordResetCode.objects.create(
            user=user,
            code=verification_code,
        )
        # sms_text = SMS_TEXTS['verify_code'].format(verification_code)
        # send_sms(user.phone_number, sms_text)
        self.request.session['phone_number'] = user.phone_number
        return user








class PasswordResetForm(forms.Form):
    phone_number = forms.CharField(
        label='شماره تلفن همراه',
        max_length=11,
        min_length=11,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'مثال: 09123456789'})
    )

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if not User.objects.filter(phone_number=phone_number).exists():
            raise forms.ValidationError('کاربری با این شماره موبایل وجود ندارد!', code='invalid_phone')
        return phone_number


class VerifyCodeForm(forms.Form):
    code = forms.CharField(
        label='کد تأیید',
        min_length=6,
        max_length=6,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'کد دریافتی را وارد کنید'})
    )

    def __init__(self, phone_number, *args, **kwargs):
        self.phone_number = phone_number
        super().__init__(*args, **kwargs)

    def clean_code(self):
        code = self.cleaned_data.get('code')
        try:
            user = User.objects.get(phone_number=self.phone_number)
            reset_code = PasswordResetCode.objects.filter(user=user, code=code, is_used=False).first()
            if not reset_code or not reset_code.created_at:
                raise forms.ValidationError('کد وارد شده نامعتبر یا منقضی شده است', code='invalid_code')
        except User.DoesNotExist:
            raise forms.ValidationError('کاربر یافت نشد', code='invalid_user')
        return code



class ResetPasswordForm(forms.Form):
    new_password = forms.CharField(
        max_length=100,
        min_length=8,
        label='رمز عبور جدید',
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'رمز عبور جدید'})
    )
    confirm_password = forms.CharField(
        max_length=100,
        min_length=8,
        label='تکرار رمز عبور جدید',
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'تکرار رمز عبور'})
    )

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')
        if new_password and confirm_password and new_password != confirm_password:
            raise forms.ValidationError('رمزها با هم مطابقت ندارند!', code='password_mismatch')
        return cleaned_data


class RegistrationVerifyCodeForm(forms.Form):
    code = forms.CharField(
        label='کد تأیید ثبت‌نام',
        min_length=6,
        max_length=6,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'کد دریافتی را وارد کنید'})
    )

    def __init__(self, phone_number, *args, **kwargs):
        self.phone_number = phone_number
        super().__init__(*args, **kwargs)

    def clean_code(self):
        code = self.cleaned_data.get('code')
        try:
            user = User.objects.get(phone_number=self.phone_number)
            reset_code = PasswordResetCode.objects.filter(user=user, code=code, is_used=False,).first()
            if not reset_code or not reset_code.created_at:
                raise forms.ValidationError('کد وارد شده نامعتبر یا منقضی شده است', code='invalid_code')
        except User.DoesNotExist:
            raise forms.ValidationError('کاربر یافت نشد', code='invalid_user')
        return code

