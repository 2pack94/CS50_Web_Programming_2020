from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:page>", views.page, name="wiki_page"),
    path("edit/<str:page>", views.editPage, name="edit_page"),
    path("new", views.newPage, name="new_page"),
    path("random", views.randomPage, name="random_page"),
]
