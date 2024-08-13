from django.urls import path , include
from .views import chatbot

urlpatterns = [
    path('chatbot' , chatbot , name='chatbot' ),
    
]
