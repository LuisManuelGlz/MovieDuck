from django.urls import path
from . import views

app_name = 'registration'
urlpatterns = [
  path('signup/', views.Signup.as_view(), name='signup'),
  path('me/', views.ProfileUpdate.as_view(), name='profile'),
  path('settings/', views.AccountUpdate.as_view(), name='account'),
  # path('name_change/', views.NameUpdate.as_view(), name='name-change'),
]