"""
URL configuration for api app.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
"""
from django.urls import path
from .views import *




urlpatterns = [
    path('books/', books, name='books'),
    path('borrow/', borrow_book, name='borrow_book'),
    path('return/', return_book, name='return_book'),
    path('borrowed/<int:borrower_id>/', get_active, name='active_borrow'),
    path('history/<int:borrower_id>/', get_history, name='borrow_history'),
]