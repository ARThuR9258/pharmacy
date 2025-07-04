from django import forms
from .models import Drugs

class DrugForm(forms.ModelForm):
    class Meta:
        model = Drugs
        fields = ['name' , 'number' , 'category' , 'expiration_date' , 'description' , 'date_in_warehouse']
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
            'placeholder': 'دسته بندی دارو '
            }),

            'expiration_date': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'تاریخ انقضا دارو'
            }),

            'description': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'توضیحات برای این دارو'
            }),
            'date_in_warehouse': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'تاریخ ورود به انبار'
            }),

        }