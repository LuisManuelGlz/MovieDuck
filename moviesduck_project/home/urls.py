from django.urls import path
from home import views 

# Url para la app home

urlpatterns = [
    path ('',views.Home.as_view(),name= 'home'),
    path('about/', views.about.as_view(), name='about'),

]