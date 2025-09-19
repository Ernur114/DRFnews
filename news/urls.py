from django.urls import path
from .views import update_articles, list_articles

urlpatterns = [
    path("articles/update/", update_articles),
    path("articles/", list_articles),
]
