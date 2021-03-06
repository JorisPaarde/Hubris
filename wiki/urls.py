"""
URL patterns for the Wiki app
"""

from django.urls import path
from . import views

app_name = "wiki"

urlpatterns = [
    path('', views.wiki, name='wiki'),
]
