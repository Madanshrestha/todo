from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import CreateView, FormView

from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy

from .models import User
from .form import CustomUserRegistrationForm


# Create your views here.
class CustomLoginView(LoginView):
    template_name = 'account/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tasks')
    

class CustomRegisterView(CreateView):
    form_class = CustomUserRegistrationForm
    model = User
    # fields = ['email', 'name', 'password', 'password2', 'tc', 'profile_image']
    template_name = 'account/register.html'
    redirect_authenticated_user = True
    success_url = reverse_lazy("tasks")

    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        print(form.errors)
    
    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(CustomRegisterView, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(CustomRegisterView, self).get(*args, **kwargs)
    # def post(self, *args, **kwargs):
    #     print(self.request.POST)
    
