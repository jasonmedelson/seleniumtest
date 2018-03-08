from django.urls import path
from . import views
from django.conf.urls import url


urlpatterns = [
    path("", views.index, name="index"),
    url(r'^search/$', views.search),
    url(r'^yt/$', views.yt, name="yt"),
    url(r'^yt/youtube/$', views.youtube),
    url(r'^twinge/$', views.twinge, name="twinge"),
    url(r'^twinge/data/$', views.twingedata),
    url(r'^search-form/$', views.index),

]