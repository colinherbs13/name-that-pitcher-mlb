from django.urls import re_path

from . import views

urlpatterns = [
    re_path(r'^$', views.GameView.as_view(), name='game'),
]
