from django.urls import path , include
from .views import home , login_view , logout_view , predict_view 


urlpatterns = [
    path('' , home , name='home' ),
    path('login/' , login_view , name='login' ),
    path('logout/' , logout_view , name='logout' ),
    path('weather/' , predict_view , name='weather' ),
    
]
