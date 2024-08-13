from django.shortcuts import render , redirect
from django.contrib.auth import authenticate , login , logout
from django.contrib import messages

from .weatherAPI import weather

# Create your views here.
def home(request):
    
    return render(request , "pages/index.html" )



def login_view(request):
    
    if request.method == "POST":
        username = request.POST["userName"] # name = "userName" in the login.html
        password = request.POST["password"] # name = "password" in the login.html
        
        
        print(username , password)
        user = authenticate(request, username=username, password=password)
        
        
        
        if user is not None:
            login(request, user)
            messages.success(request, "User login Success")
            # rerdirect
            print("login")
            
            return redirect( "home" )
        
        else:
            messages.success(request, "User Not login ")
            return redirect("login")

    return render(request , "auth/login.html")


def logout_view(request):
    logout(request)
    
    return redirect('home')


def predict_view(request):
    context = None
    
    if request.method == "POST":
        location= request.POST['location']
        
        data =  weather(location)
        
        
        
        name = data['location']['name']
        temperature = data['data']['values']['temperature']
        humidity = data['data']['values']['humidity']
        dew_point = data['data']['values']['dewPoint']
        rain_intensity = data['data']['values']['rainIntensity']
        uv_index = data['data']['values']['uvIndex']
        wind_speed = data['data']['values']['windSpeed']
        date_time = data['data']['time']
        
        
        context= {
            'location':name,
            'temperature':temperature,
            'humidity':humidity,
            'dewpoint':dew_point,
            'rain_intensity':rain_intensity,
            'uv_index':uv_index,
            'wind_speed':wind_speed,
            
        }
        
        return render(request , "weather/apiINFO.html" , context)

        
    return render(request , "weather/weather_app.html")


