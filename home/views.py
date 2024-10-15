from django.shortcuts import render , HttpResponse , redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
# Create your views here.
def home_page(request):
    return render(request,"home/index.html")

def register_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email= request.POST.get("email")
        password = request.POST.get("password")
        if User.objects.filter(email=email).exists():
          return HttpResponse("email already exists!")
        else:
            user = User.objects.create_user(username=username,email=email,password=password)
            user.save()
            return redirect(request,"/dashboard/")
    return render(request,"home/register.html")