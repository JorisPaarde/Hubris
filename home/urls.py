from django.urls import path
from . import views
from django.conf import settings

app_name = "home"

urlpatterns = [
  path("", views.main_menu, name="main-menu"),
  path("register/", views.register_request, name="register"),
  path("login/", views.login_request, name="login"),
  path("logout/", views.logout_request, name="logout"),
  path("how-to-play/", views.how_to_play, name="how-to-play"),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(
      settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
