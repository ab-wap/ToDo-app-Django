from django import forms
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