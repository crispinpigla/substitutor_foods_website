from django.conf.urls import include, url

from django.urls import path

from . import views  # import views so we can use them in urls.

def trigger_error(request):
    division_by_zero = 1 / 0





urlpatterns = [
    path("", views.redirect_home),
    path('sentry-debug/', trigger_error),
    url("home/", views.home),
    url("substitute/", views.substitute),
    url(r"^(?P<product_id>[0-9]+)/$", views.detail),
    url("favoris/", views.favoris),
    url("account/", views.account),
    url("delete/", views.delete),
    url(r"^([a-z]+)/", views.errorrr_404),
]
