from django.urls import path
from . import views


urlpatterns = [
    path('video', views.download_view, name='download'),
]