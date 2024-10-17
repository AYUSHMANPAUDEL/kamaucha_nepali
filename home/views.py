from django.shortcuts import render , HttpResponse , redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate , login , logout
from django.contrib import messages
from home.models import TotalDonation , Donation , PayoutRequest , Support , Annoucement
# Create your views here.
def home_page(request):
    return render(request,"home/index.html")

def register_page(request):
    if request.user.is_authenticated:
       return redirect("/dashboard/")
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
     recent_donations = Donation.objects.filter(username=request.user).order_by('-donation_date')[:5]
     try:
        total_donation = TotalDonation.objects.get(username=request.user).total_donation
     except TotalDonation.DoesNotExist:
            total_donation = 0
     payout_requests = PayoutRequest.objects.filter(username=request.user).order_by('-appeal_date')[:5]
     annoucements = Annoucement.objects.filter().order_by('-created_at')[:5]
     support_tickets = Support.objects.filter(username=request.user).order_by('-created_at')[:3]
     print(total_donation)
     return render(request,"home/dashboard.html",{"total_donation":total_donation ,"recent_donations": recent_donations,"payout_requests":payout_requests,"support_tickets":support_tickets,"annoucements":annoucements})
    return redirect("/login/")

def logout_page(request):
   if request.user.is_authenticated:
      logout(request)
      return redirect("/login/")
   return redirect("/login/")

def support_page(request):
    if not request.user.is_authenticated:
        return redirect("/login/")
    if request.method == "POST":
        ticket_title = request.POST.get("title")
        discord_id = request.POST.get("discordid")
        support_message = request.POST.get("support_message")
        print(ticket_title, discord_id, support_message)
        support_db = Support.objects.create(
            username=request.user,
            ticket_title=ticket_title,
            discord_id=discord_id,
            support_message=support_message # Assuming you have a status field in your model
        )
        support_db.save()
        messages.success(request, "We have received your message! We will reply to you on Discord shortly.")
        return redirect("support_page")  # Redirect to prevent resubmission
    else:
        # Fetch user's previous support tickets
        support_tickets = Support.objects.filter(username=request.user).order_by('-created_at')
        return render(request, "home/support.html", {'support_tickets': support_tickets})

def donation_page_setup(request):
    if request.user.is_authenticated:
        return render(request,"home/donation_setup_page.html")
    return redirect("/login/")

def alert_setup_page(request):
    if request.user.is_authenticated:
        return render(request,"home/alert_setup.html")
def payout_request_page(request):
    if request.user.is_authenticated:
        return render(request,"home/payout_request.html")
    return redirect("/login/")
    
def transcations_history_page(request):
    if request.user.is_authenticated:
        return render(request,"home/transcations_history.html")
    return redirect("/login/")

def donations_page(request):
    if request.user.is_authenticated:
        return render(request,"home/donations.html")
    return redirect("/login/")