from django.conf.urls import include

from django.urls import path, re_path

from . import views  # import views so we can use them in urls.


urlpatterns = [
    path("", views.redirect_home),
    re_path(r"home(?:/|)", views.home),
    re_path("substitute/", views.substitute),
    re_path(r"^(?P<product_id>[0-9]+)(?:/|)$", views.detail),
    re_path("favoris/", views.favoris),
    re_path("account/", views.account),
    re_path("delete/", views.delete),
    re_path("comments/", views.comments),
    re_path(r"([a-z]+)/", views.errorrr_404),
]
