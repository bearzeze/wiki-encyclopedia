from django.urls import path

from . import views

app_name = "encyclopedia"

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.wiki, name="wiki"),
    path("wiki/search/", views.search, name="search"),
    path("new-page", views.new_page, name="new_page"),
    path("edit/<str:title>", views.edit_page, name="edit_page"),
    path("delete/<str:title>", views.delete_page, name="delete_page"),
    path("random/", views.random_page, name="random_page"),

]
