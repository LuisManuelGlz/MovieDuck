from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Profile
# from .widgets import AvatarField

class UserCreationFormWithEmail(UserCreationForm):
  first_name = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'form-control form-control-user', 'placeholder': 'First name', 'autofocus': True}))
  last_name = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'form-control form-control-user', 'placeholder': 'Last name'}))
  username = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'form-control form-control-user', 'placeholder': 'Username'}))
  email = forms.CharField(label='', widget=forms.EmailInput(attrs={'class': 'form-control form-control-user', 'placeholder': 'Email Address'}))
  password1 = forms.CharField(label='', widget=forms.PasswordInput(attrs={'class': 'form-control form-control-user', 'placeholder': 'Password'}))
  password2 = forms.CharField(label='', widget=forms.PasswordInput(attrs={'class': 'form-control form-control-user', 'placeholder': 'Confirm Password'}))
  
  class Meta:
    model = User
    fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2',]

  def clean_first_name(self):
    first_name = self.cleaned_data.get('first_name')
    if not len(first_name) > 0:
      raise forms.ValidationError("I know that's not your first name")
    return first_name.strip()

  def clean_last_name(self):
    last_name = self.cleaned_data.get('last_name')
    if not len(last_name) > 0:
      raise forms.ValidationError("I know that's not your last name")
    return last_name.strip()

  def clean_email(self):
    email = self.cleaned_data.get('email')
    if User.objects.filter(email=email).exists():
      raise forms.ValidationError('A user with that email already exists.')
    return email

class ProfileForm(forms.ModelForm):
  location = forms.CharField(label='Location', required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Location',}))
  bio = forms.CharField(label='Bio', required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Bio', 'rows': False, 'style':'resize:none;'}))
  avatar = forms.ClearableFileInput(attrs={'class': 'form-control-file'})

  class Meta:
    model = Profile
    fields = ['location', 'bio', 'avatar',]

class AccountForm(forms.ModelForm):
  first_name = forms.CharField(max_length=25, label='',widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Firts Name'}))
  last_name = forms.CharField(max_length=35, label='', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}))
  email = forms.CharField(label='', widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email', 'autofocus': True}))
  
  class Meta:
    model = User
    fields = ['first_name', 'last_name', 'email',]

  def clean_first_name(self):
    first_name = self.cleaned_data.get('first_name')
    if not len(first_name) > 0:
      raise forms.ValidationError("I know that's not your first name")
    return first_name.strip()

  def clean_last_name(self):
    last_name = self.cleaned_data.get('last_name')
    if not len(last_name) > 0:
      raise forms.ValidationError("I know that's not your last name")
    return last_name.strip()

  def clean_email(self):
    email = self.cleaned_data.get('email')
    if 'email' in self.changed_data:
      if User.objects.filter(email=email).exists():
        raise forms.ValidationError('A user with that email already exists.')
    return email
