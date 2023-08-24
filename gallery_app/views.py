from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request,'main/index.html')

def admin(request):
    return render(request,'administrator/index.html')