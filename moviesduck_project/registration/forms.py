from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Profile

class UserCreationFormWithEmail(UserCreationForm):
  username = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username', 'autofocus': True}))
  email = forms.CharField(label='', widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
  password1 = forms.CharField(label='', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
  password2 = forms.CharField(label='', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm password'}))
  
  class Meta:
    model = User
    fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2',]

  def clean_email(self):
    email = self.cleaned_data.get('email')
    if User.objects.filter(email=email).exists():
      raise forms.ValidationError('A user with that email already exists.')
    return email

class ProfileForm(forms.ModelForm):
  avatar = forms.ClearableFileInput(attrs={'class': 'form-control-file'})

  class Meta:
    model = Profile
    fields = ['avatar',]


class EmailForm(forms.ModelForm):
  email = forms.CharField(label='', widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email', 'autofocus': True}))
  first_name = forms.CharField(max_length=25, label='',widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Firts Name', 'autofocus': True}))
  last_name = forms.CharField(max_length=35, label='', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name', 'autofocus': True}))
  
  class Meta:
    model = User
    fields = ['email', 'first_name', 'last_name', ]

  def clean_email(self):
    email = self.cleaned_data.get('email')
    if 'email' in self.changed_data:
      if User.objects.filter(email=email).exists():
        raise forms.ValidationError('A user with that email already exists.')
    return email


  def clean_first_name(self):
    first_name = self.cleaned_data.get('first_name')
    if not first_name.isalpha():
      raise forms.ValidationError('The name not is valid')
    return first_name


  def clean_last_name(self):
    last_name = self.cleaned_data.get('last_name')
    if not last_name.isalpha():
      raise forms.ValidationError('The last name not is valid')
    return last_name  






  