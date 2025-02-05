from django.shortcuts import render

# Create your views here.

def portfoilio_page(request):
    return render(request, 'portfolio/portfolio.html')