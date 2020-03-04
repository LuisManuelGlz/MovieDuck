from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.
# Se creo la vista de home

class Home(TemplateView):
    template_name = 'home/home.html'

class about (TemplateView):
    template_name = 'home/about.html'