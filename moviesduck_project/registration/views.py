from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import (
  UserCreationFormWithEmail,
  ProfileForm,
  AccountForm
)
from .models import Profile

class Signup(generic.CreateView):
  template_name = 'registration/signup.html'
  form_class = UserCreationFormWithEmail
  success_url = reverse_lazy('login')

  def get(self, request, *args, **kwargs):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse_lazy('home:home'))
    return super(Signup, self).get(request, *args, **kwargs)

class ProfileUpdate(LoginRequiredMixin, generic.UpdateView):
  form_class = ProfileForm
  success_url = reverse_lazy('registration:profile')
  
  def get_object(self):
    profile, created = Profile.objects.get_or_create(user=self.request.user)
    return profile

class AccountUpdate(LoginRequiredMixin, generic.UpdateView):
  template_name = 'registration/account_form.html'
  form_class = AccountForm
  success_url = reverse_lazy('registration:account')

  def get_object(self):
    return self.request.user

class NameUpdate(LoginRequiredMixin, generic.UpdateView):
  template_name = 'registration/name_form.html'
  form_class = AccountForm
  success_url = reverse_lazy('registration:profile')

  def get_object(self):
    return self.request.user
