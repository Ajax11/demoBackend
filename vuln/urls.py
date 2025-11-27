from django.urls import path
from . import views

urlpatterns = [
    path("ping/", views.run_ping),
    path("user/", views.get_user),
]
