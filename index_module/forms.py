from django import forms
from .models import Drugs

class DrugForm(forms.ModelForm):
    class Meta:
        model = Drugs
        fields = ['name', 'number', 'category', 'expiration_date', 'description', 'date_in_warehouse']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'نام دارو'
            }),
            'number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'تعداد دارو'
            }),
            'category': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'دسته بندی دارو'
            }),
            'expiration_date': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'YYYY/MM (مثال: 2025/10)',
                'id': 'expiration-date-input'  # ID برای جاوااسکریپت
            }),
            'description': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'توضیحات برای این دارو'
            }),
            'date_in_warehouse': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'تاریخ ورود به انبار',
                'type': 'text'
            }),
        }

    def clean_expiration_date(self):
        expiration_date = self.cleaned_data.get('expiration_date')
        if expiration_date:
            try:
                year, month = map(int, expiration_date.split('/'))
                if not (1 <= month <= 12 and 1900 <= year <= 2100):  # محدوده منطقی
                    raise ValueError
                # تبدیل به تاریخ کامل (روز اول ماه) برای سازگاری با DateField
                expiration_date = f"{year}-{month:02d}-01"
                self.cleaned_data['expiration_date'] = expiration_date
            except (ValueError, AttributeError):
                raise forms.ValidationError("فرمت تاریخ انقضا باید YYYY/MM باشد (مثال: 2025/10).")
        return expiration_date