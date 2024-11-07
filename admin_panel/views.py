from django.shortcuts import render , redirect , HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
# Create your views here.
def admin_login(request):
    if request.user.is_superuser:
        return redirect("admin_dashboard")
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request,username=username,password=password)
        if user is not None:
            if user.is_superuser:
                login(request,user)
                return redirect("admin_dashboard")
            else:
                messages.error(request,"You are not one of our staffs")
                return redirect("admin_login")
        else:
            messages.error(request,"User not found")
            return redirect("admin_login")
    return render(request , "admin_panel/login.html")

def admin_dashboard(request):
    if request.user.is_superuser:
         return render(request,"admin_panel/admin_dashboard.html")
    return redirect("admin_login")