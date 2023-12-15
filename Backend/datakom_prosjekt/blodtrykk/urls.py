from django.urls import path

from . import views

urlpatterns = [
    path("blodtrykk", views.test2, name="først test"),
]
