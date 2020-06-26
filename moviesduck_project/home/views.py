from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
# Se creo la vista de home

class Home(LoginRequiredMixin, TemplateView):
    template_name = 'home/home.html'

class about (TemplateView):
    template_name = 'home/about.html'