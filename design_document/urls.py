from django.test import TestCase

# Create your tests here.
from django.urls import path


from . import views

urlpatterns = [
    path('look_and_download_dd', views.look_and_download_dd, name='look_and_download_dd')
    
]
