from django.urls import path

from . import views

# app_name = "wiki"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry>", views.wiki, name='wiki'),
    path("search", views.search, name="search"),
    path("create", views.new_entry, name="create")
]
