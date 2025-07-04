# from django.urls import path 
# from .views import support , ai_chatbot

# urlpatterns = [
#     path('support' , support , name='support' ),
#     path('ask' , ai_chatbot , name='ai_chatbot' ),
    
# ]
from django.urls import path
from .views import ChatAPIView

urlpatterns = [
    path('chat/', ChatAPIView.as_view(), name='chat_api'),
]
