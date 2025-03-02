from django.shortcuts import render

# Create your views here.
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from .models import CustomUser

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("dashboard")
    return render(request, "users/login.html")

def logout_view(request):
    logout(request)
    return redirect("login")
