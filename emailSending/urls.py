"""
This file is used to define the URL patterns for the contact app.
"""
from django.urls import path
from .views import SendEmailView

urlpatterns = [
    path('sendEmail/', SendEmailView.as_view(), name='sendEmail'),
]
