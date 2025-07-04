from django import forms
from .models import User

class SignUpForm(forms.ModelForm):
    password2 = forms.CharField(max_length=100, required=True, widget=forms.PasswordInput(), label='تکرار رمز عبور')

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
                'error_message': 'شماره موبایل وارد شده معتبر نیست'
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
        return user











#
# class PasswordResetForm(forms.ModelForm):
#         phone = forms.CharField(label='شماره موبایل کاربر', required=True, min_length=11,
#                                 max_length=11,)
#
#         class Meta:
#             model = User
#             fields = ['phone']
#
#         def __init__(self, *args, **kwargs):
#             self.request = kwargs.pop('request')
#             super().__init__(*args, **kwargs)
#
#         def clean_phone(self):
#             if not User.objects.filter(phone=self.cleaned_data.get('phone')).exists():
#                 raise forms.ValidationError('کاربری با این شماره موبایل وجود ندارد!', code='phone')
#
#             return self.cleaned_data['phone']

