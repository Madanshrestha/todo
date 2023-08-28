from django import forms

from .models import Task

class TaskForm(forms.Form):
    title = forms.CharField(max_length=200)
    description = forms.Textarea()
    complete = forms.BooleanField()
