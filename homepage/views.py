from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'index.html')

def vendor_home(request):
    return render(request,'vendor_home.html')
