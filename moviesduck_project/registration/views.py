from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserCreationFormWithEmail, ProfileForm, EmailForm
from .models import Profile

class Signup(generic.CreateView):
  template_name = 'registration/signup.html'
  form_class = UserCreationFormWithEmail
  success_url = reverse_lazy('login')

class ProfileUpdate(LoginRequiredMixin, generic.UpdateView):
  form_class = ProfileForm
  success_url = reverse_lazy('registration:profile')
  
  def get_object(self):
    profile, created = Profile.objects.get_or_create(user=self.request.user)
    return profile

class EmailUpdate(LoginRequiredMixin, generic.UpdateView):
  template_name = 'registration/email_form.html'
  form_class = EmailForm
  success_url = reverse_lazy('registration:profile')

  def get_object(self):
    return self.request.user