from django.shortcuts import render , HttpResponse , redirect , HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate , login , logout
from django.contrib import messages
from home.models import TotalDonation , Donation , PayoutRequest , Support , Annoucement , Alert , Donation_page
import uuid
import hashlib
import hmac
import base64
import json
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.conf import settings
import requests
# Create your views here.
def home_page(request):
    if request.user.is_authenticated:
        return redirect("dashboard_page")
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
        elif User.objects.filter(username=username).exists():
          messages.error(request, "Username Already Exists!")
          return redirect("register_page") 
        else:
            user = User.objects.create_user(username=username,first_name=first_name,last_name=last_name,email=email,password=password)
            user.save()
            login(request,user)
            messages.success(request, "You have successfully created your account . Please Remember your username for future use.")
            return redirect("/dashboard/")
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
            return redirect("/dashboard/")
        else:
            messages.error(request, "Invalid Username or password.")
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
     return render(request,"home/dashboard.html",{"total_donation":total_donation ,"recent_donations": recent_donations,"payout_requests":payout_requests,"support_tickets":support_tickets,"annoucements":annoucements})
    return redirect("/login/")

def logout_page(request):
   if request.user.is_authenticated:
      logout(request)
      return redirect("home_page")
   return redirect("/login/")

def support_page(request):
    if not request.user.is_authenticated:
        return redirect("/login/")
    if request.method == "POST":
        ticket_title = request.POST.get("title")
        discord_id = request.POST.get("discordid")
        support_message = request.POST.get("support_message")
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
        # Fetch existing donation page details
        donation_page_details = Donation_page.objects.get(username=request.user)
        alert_details = Alert.objects.get(username = request.user) #------>alert_id ra latest donation herne ma chaine id autaai ho !

        if request.method == "POST":
            # Get uploaded file and donation message from the request
            profile_picture = request.FILES.get("profile_picture")  # Use request.FILES for file uploads
            page_message = request.POST.get("donation_message")

            # Update donation page details
            if profile_picture:
                donation_page_details.profile_picture = profile_picture  # Set new profile picture if provided

            donation_page_details.page_message = page_message  # Update donation message

            # Save the updated donation page details
            donation_page_details.save()

            return redirect("donation_setup_page")

        return render(request, "home/donation_setup_page.html", {"donation_page_details": donation_page_details , "alert_details":alert_details})

    return redirect("/login/")

def alert_setup_page(request):
    if request.user.is_authenticated:
        current_alert = Alert.objects.get(username=request.user)

        if request.method == 'POST':
            if 'alert_image_1' in request.FILES:
                current_alert.alert_image_level_1 = request.FILES['alert_image_1']
            if 'alert_image_2' in request.FILES:    
                current_alert.alert_image_level_2 = request.FILES['alert_image_2']
            if 'alert_image_3' in request.FILES:
                current_alert.alert_image_level_3 = request.FILES['alert_image_3']
            if 'alert_sound_1' in request.FILES:
                 current_alert.alert_sound_1 = request.FILES['alert_sound_1']
            if 'alert_sound_2' in request.FILES:
                 current_alert.alert_sound_2 = request.FILES['alert_sound_2']
            if 'alert_sound_3' in request.FILES:
                 current_alert.alert_sound_3 = request.FILES['alert_sound_3']


            
            current_alert.save()  # Save the instance with the new images
       
            return redirect('alert_setup_page')  # Redirect to the same page after saving

        return render(request, "home/alert_setup.html", {"current_alert": current_alert})

    return redirect('login_page')

def payout_request_page(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            username = request.user
            payout_amount = request.POST.get('amount')
            payout_method = request.POST.get('payment_method')
            payout_account = request.POST.get('payment_account')
            request_payout = PayoutRequest.objects.create(username=username,payout_account=payout_account,payout_method=payout_method,payout_amount=payout_amount)
            request_payout.save()
            messages.success(request,"We have got your payout request.")
            return redirect("payout_request_page")
    
        try:
         total_donation = TotalDonation.objects.get(username=request.user).total_donation
        except TotalDonation.DoesNotExist:
         total_donation = 0
        payout_requests = PayoutRequest.objects.filter(username=request.user).order_by('-appeal_date')
        return render(request,"home/payout_request.html",{"total_donation":total_donation , "payout_requests":payout_requests})
    return redirect("/login/")

    
def transcations_history_page(request):
    if request.user.is_authenticated:
        completed_transactions = PayoutRequest.objects.filter(username=request.user).order_by('-appeal_date')
        return render(request,"home/transcations_history.html", {'transactions': completed_transactions})
    return redirect("/login/")

def donations_page(request):
    if request.user.is_authenticated:
        recent_donations = Donation.objects.filter(username=request.user).order_by('-donation_date')[:30]
        return render(request,"home/donations.html",{"recent_donations":recent_donations})
    return redirect("/login/")

def alert_page(request ,alert_id):
    if Alert.objects.filter(alert_id=alert_id).exists():
        alert_detail = Alert.objects.get(alert_id=alert_id)
        return render(request,"home/alert_page.html",{"alert_detail":alert_detail})
    return HttpResponse("404 PAGE NOT FOUND")

def generate_signature(amount, transaction_uuid, product_code, secret_key):
    data = f"total_amount={amount},transaction_uuid={transaction_uuid},product_code={product_code}"
    hmac_signature = hmac.new(secret_key.encode('utf-8'), data.encode('utf-8'), hashlib.sha256).digest()
    signature = base64.b64encode(hmac_signature).decode('utf-8')
    return signature


def donate_page(request, username):
    if User.objects.filter(username=username).exists():
        if request.method == "POST":
            method = request.POST.get("method")
            amount = int(request.POST.get("donation_amount"))
            if (amount <= 10):
                messages.error(request,"Donation amount must be greater than Rs.10")
                return redirect("donate_page",username=username)
            if method == "esewa":
                donator_name = request.POST.get("donator_name")
                donation_amount = int(request.POST.get('donation_amount'))
                donation_message = request.POST.get('donation_message')
                transaction_uuid = 'TXN_' + str(uuid.uuid4())
                secret_key = "8gBm/:&EnhH.1/q"  # Ensure this is correct
                product_code = "EPAYTEST"
                user = User.objects.get(username=username)
                donation = Donation.objects.create(username=user,donator_name=donator_name,donation_message=donation_message,donation_amount=donation_amount,transaction_uuid=transaction_uuid)
                donation.save()
                # Generate the data string for signature
                signature = generate_signature(donation_amount, transaction_uuid, product_code, secret_key)
                # Prepare context for the redirect page
                context = {
                'amount': donation_amount,  # Example amount
                'transaction_uuid': transaction_uuid,
                'product_code': product_code,
                'signature': signature
                }
                

                # Render the esewa_redirect.html with the context
                return render(request, "home/esewa_redirect.html", context)
            else:
                donator_name = request.POST.get("donator_name")
                donation_amount = int(request.POST.get('donation_amount'))*100  
                donation_message = request.POST.get('donation_message')
                transaction_uuid = 'TXN_' + str(uuid.uuid4())
                secret_key = "8gBm/:&EnhH.1/q"  # Ensure this is correct
                product_code = "EPAYTEST"
                user = User.objects.get(username=username)
                donation = Donation.objects.create(username=user,donator_name=donator_name,donation_message=donation_message,donation_amount=donation_amount/100,transaction_uuid=transaction_uuid)
                donation.save()


                url = "https://a.khalti.com/api/v2/epayment/initiate/"

                payload = json.dumps({
                    "return_url": "http://127.0.0.1:8000/khalti/success",
                    "website_url": "http://127.0.0.1:8000/",
                    "amount": donation_amount,
                    "purchase_order_id": transaction_uuid,
                    "purchase_order_name": donator_name,
                })
                headers = {
                    'Authorization': f'key {settings.KHALTI_SECRET_KEY}',
                    'Content-Type': 'application/json',
                }
    
                response = requests.request("POST", url, headers=headers, data=payload)

                if response.status_code == 200:
                            response_data = response.json()
                            payment_url = response_data.get('payment_url')

                            # Add the payment_url to the context for the Khalti redirect page
                            context = {
                                'payment_url': payment_url
                            }

                            return render(request, "home/khalti_redirect.html", context)
                else:
    
                    error_message = response.content.decode('utf-8')
                    return HttpResponse(f"Failed to initiate Khalti payment. Error: {error_message}")
        # Fetch user data for GET request
        user = User.objects.get(username=username)
        alert_detail = Alert.objects.get(username=user)
        donation_page_details = Donation_page.objects.get(username=user)
        donators = Donation.objects.filter(username=user,donation_status="Completed").order_by('-donation_amount')[:10]
        return render(request, "home/donate_page.html", {
            "alert_detail": alert_detail,
            "donation_page_details": donation_page_details,
            "donators": donators , 
        })

    return HttpResponse("404 Page not found!")

def esewa_success(request):
    encoded_data = request.GET.get('data')
    decoded_data = base64.b64decode(encoded_data).decode('utf-8')
    payment_data = json.loads(decoded_data)
    transaction_code = payment_data.get('transaction_code')
    status = payment_data.get('status')
    total_amount = payment_data.get('total_amount')
    transaction_uuid = payment_data.get('transaction_uuid')
    product_code = payment_data.get('product_code')
    try:
        transaction = Donation.objects.get(transaction_uuid=transaction_uuid)
        username = transaction.username
        user = User.objects.get(username=username)
        transaction.donation_status = 'Completed'  # Update the status
        transaction.save()
        alert = Alert.objects.get(username=user)
        alert_id = alert.alert_id
        return render(request,"home/esewa_success.html",{"transcation":transaction , "alert_id":alert_id})
    except Donation.DoesNotExist:
        return HttpResponse("Error Occured")
    return redirect("/")

def khalti_success(request):
    transaction_uuid = request.GET.get('purchase_order_id') 
    try:
        transaction = Donation.objects.get(transaction_uuid=transaction_uuid)
        username = transaction.username
        user = User.objects.get(username=username)
        transaction.donation_status = 'Completed'  # Update the status
        transaction.save()
        alert = Alert.objects.get(username=user)
        alert_id = alert.alert_id
        return render(request,"home/khalti_success.html",{"transcation":transaction , "alert_id":alert_id})
    except Donation.DoesNotExist:
        return HttpResponse("Error Occured")
    return redirect("/")

def latest_donations_preview(request,alert_id):
    if Alert.objects.filter(alert_id=alert_id).exists():
        alert_detail = Alert.objects.get(alert_id=alert_id)
        return render(request,"home/latest_donations_page.html",{"alert_detail":alert_detail})
    return HttpResponse("404 PAGE NOT FOUND")

def live_donations_preview(request,alert_id):
    if Alert.objects.filter(alert_id=alert_id).exists():
        alert_detail = Alert.objects.get(alert_id=alert_id)
        return render(request,"home/live_donations.html",{"alert_detail":alert_detail})
    return HttpResponse("404 PAGE NOT FOUND")