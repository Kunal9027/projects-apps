from django.urls import path , include
from .views import chatbot

urlpatterns = [
    path('chefbot' , chatbot , name='chiefbot' ),
    
]
