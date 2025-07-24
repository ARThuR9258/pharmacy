from django import forms
from .models import DailySale


class DailySaleForm(forms.ModelForm):
    class Meta:
        model = DailySale
        fields = ['date' , 'day' , 'cash' , 'pose_device' , 'mobile_payment' , 'result']
        widgets = {
            'date': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'مثال: 1404/05/02'
            }),
            'day': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'مثال: چهارشنبه'
            }),
            'cash': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'مثال: 965,000 تومان'
            }),
            'pose_device': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'مثال: 16,850,000 تومان'
            }),
            'mobile_payment': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'مثال: 2,400,000 تومان'
            }),
            'result': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'مثال: 20,215,000 تومان'
            }),
        }
