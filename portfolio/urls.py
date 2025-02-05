
from django.urls import path , include
from .views import portfoilio_page


urlpatterns = [
   
   path('', portfoilio_page, name='portfoilio_page'),

]