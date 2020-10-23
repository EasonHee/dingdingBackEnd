"""backend_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from esearch.views import EsearchView
from users.views import UsersView
from keywords.views import KeywordsView
from sendemail.views import EmailView
from dividends.views import DividendsView

urlpatterns = [
    path('api/esearch/', EsearchView.as_view()),
    path('api/users/', UsersView.as_view()),
    path('api/keywords/', KeywordsView.as_view()),
    path('api/emails/', EmailView.as_view()),
    path('api/dividends/', DividendsView.as_view())
]
