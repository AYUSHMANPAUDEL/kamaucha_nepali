from django.shortcuts import render , HttpResponse , redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate , login , logout
from django.contrib import messages
# Create your views here.
def home_page(request):
    return render(request,"home/index.html")

def register_page(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        email= request.POST.get("email")
        password = request.POST.get("password")
        if User.objects.filter(email=email).exists():
          messages.error(request, "Email Already Exists!")
          return render(request,"home/register.html")
        else:
            user = User.objects.create_user(username=username,first_name=first_name,last_name=last_name,email=email,password=password)
            user.save()
            return redirect("/login/")
    return render(request,"home/register.html")

def login_page(request):
    if request.user.is_authenticated:
     return redirect("/dashboard/")
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username , password=password)
        if user is not None:
            login(request,user)
            print("hello world!")
            return redirect("/dashboard/")
        else:
            messages.error(request, "Invalid email or password.")
            return render(request,"home/login.html")
    return render(request,"home/login.html")

def dashboard_page(request):
    if request.user.is_authenticated:
     return render(request,"home/dashboard.html")
    return redirect("/login/")

def logout_page(request):
   if request.user.is_authenticated:
      logout(request)
      return redirect("/login/")
   return redirect("/login/")