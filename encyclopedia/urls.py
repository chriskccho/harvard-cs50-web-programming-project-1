from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry>", views.entry, name="entry"),
    path("search", views.search, name="search"),
    path("random", views.random, name="random"),
    path("newentry", views.newentry, name="newentry"),
    path("wiki/<str:entry>/editentry", views.editentry, name="editentry")
]
