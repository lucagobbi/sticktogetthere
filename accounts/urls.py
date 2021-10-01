from django.urls import path
from . import views as v

urlpatterns = [
    path("registration/", v.registration_view, name="registration"),
    path("favourites/", v.favourites_view, name="favourites"),
]
