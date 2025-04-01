from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def home(request):

    return render(request, 'home.html') 

def signupaccount(request):

    return render(request, 'signupaccount.html')

def loginaccount(request):
    return render(request, 'loginaccount.html')

def logoutaccount(request):
    return render(request, 'logoutaccount.html')