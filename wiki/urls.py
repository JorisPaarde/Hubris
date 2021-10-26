from django.urls import path
from . import views

app_name = "wiki"

urlpatterns = [
    path('wiki/', views.wiki, name='wiki'),
]
