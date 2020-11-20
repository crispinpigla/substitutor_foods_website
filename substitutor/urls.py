from django.conf.urls import include, url

from django.urls import path

from . import views  # import views so we can use them in urls.


urlpatterns = [
    path("", views.home),
    url("home/", views.home),
    url("substitute/", views.substitute),
    url(r"^(?P<product_id>[0-9]+)/$", views.detail),
    url("favoris/", views.favoris),
    url("account/", views.account),
    url("delete/", views.delete),
    url("load/", views.load),
]
