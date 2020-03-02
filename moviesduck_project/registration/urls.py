from django.urls import path
from . import views

app_name = 'registration'
urlpatterns = [
  path('signup/', views.Signup.as_view(), name='signup'),
  path('me/', views.ProfileUpdate.as_view(), name='profile'),
  path('email_change/', views.EmailUpdate.as_view(), name='email-change'),
]