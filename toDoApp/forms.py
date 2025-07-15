from django import forms
from django.contrib.auth.models import User
from .models import Todos

class TodoForm(forms.ModelForm):
    class Meta:
        model = Todos
        fields = 'title',
        labels = {
            'title' : 'New List',
        }
        widgets = {
            'title' : forms.TextInput(attrs={
                'placeholder': 'Add a new task',
                'class': 'form-control',
            })
        }

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')
    class Meta:
        model = User
        fields = ['username', 'password', 'password_confirm']
        
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data
    
class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']