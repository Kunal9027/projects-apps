from django.shortcuts import render 
from .chatbot import chef
# Create your views here.

def chatbot(request):
    context= None
         
    
    if request.method == "POST":
        input_text= request.POST['cheif']
        
       
        
        chef_response =  chef(input_text)
        
        context= {
        "chef_response" : chef_response            
        }
        
        
        return render(request , 'ai_app/home_ai.html' , context)

    
    return render(request , 'ai_app/home_ai.html', context)