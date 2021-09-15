from django.urls import path
from . import views
from django.conf import settings

app_name = "home"

urlpatterns = [
  path("", views.main_menu, name="main_menu"),
  path("register/", views.register, name="register"),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(
      settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
