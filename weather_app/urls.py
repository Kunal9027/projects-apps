from django.urls import path , include
from .views import home , login_view , logout_view , predict_view 


urlpatterns = [
    path('weather/' , home , name='weather' ),
    path('weather/info' , predict_view , name='info' ),
    path('login/' , login_view , name='login' ),
    path('logout/' , logout_view , name='logout' ),
    
]
