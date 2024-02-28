from django.urls import path

from . import views as about_views

app_name = 'about'

urlpatterns = [
    path('author/', about_views.AuthorView.as_view(), name='author'),
    path('tech/', about_views.TechView.as_view(), name='tech'),
]
