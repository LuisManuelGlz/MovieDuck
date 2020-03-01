from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from .forms import UserCreationFormWithEmail

class Signup(generic.CreateView):
  template_name = 'registration/signup.html'
  form_class = UserCreationFormWithEmail
  success_url = reverse_lazy('login')
