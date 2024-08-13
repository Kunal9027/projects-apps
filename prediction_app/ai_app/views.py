from django.shortcuts import render 

# Create your views here.

def chatbot(request):
    
    return render(request , 'ai_app/home_ai.html')