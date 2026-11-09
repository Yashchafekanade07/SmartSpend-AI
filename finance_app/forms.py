from django import forms
from .models import Expense, Budget
from django.contrib.auth.models import User

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['title', 'amount', 'category', 'date', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['category', 'monthly_limit', 'month', 'year']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-select'}),
            'monthly_limit': forms.NumberInput(attrs={'class': 'form-control'}),
            'month': forms.NumberInput(attrs={'class': 'form-control'}),
            'year': forms.NumberInput(attrs={'class': 'form-control'}),
        }
