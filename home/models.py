from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
import random
import string
# Create your models here.
class Donation(models.Model):
    PENDING = 'Pending'
    Completed = 'Completed'
    Status_Choices = [
        (PENDING, 'Pending'),
        (Completed, 'Completed'),]
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    donator_name = models.TextField(max_length=200)
    donation_amount = models.IntegerField()
    donation_date = models.DateField(auto_now_add=True)
    donation_message = models.TextField(default="")
    transaction_uuid = models.TextField(default="")
    donation_status = models.CharField(
        max_length=20,
        choices=Status_Choices,
        default=PENDING,
    )

    def __str__(self):
        return f"{self.username}"
    
class TotalDonation(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    total_donation = models.IntegerField(default=0)
    def __str__(self):
     return f"{self.username}"


@receiver(post_save, sender=Donation)
def update_total_donations(sender, instance, created, **kwargs):
    if created:
        # Get or create TotalDonation for the user
        total_donations, _ = TotalDonation.objects.get_or_create(username=instance.username)
        
        # Update the total donation amount
        total_donations.total_donation += instance.donation_amount
        total_donations.save()

class PayoutRequest(models.Model):
    PENDING = 'Pending'
    APPROVED = 'Approved'
    REJECTED = 'Rejected'
    COMPLETED = 'Completed'
    PAYOUT_STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (APPROVED, 'Approved'),
        (REJECTED, 'Rejected'),
        (COMPLETED, 'Completed'),
    ]
    
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    payout_amount = models.IntegerField()
    payout_account = models.TextField()
    payout_method = models.TextField()
    payout_status = models.CharField(
        max_length=20,
        choices=PAYOUT_STATUS_CHOICES,
        default=PENDING,
    )
    appeal_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.username}"
    

class Support(models.Model):
    PENDING = 'Pending'
    Resolved = 'Resolved'
    Closed = 'Closed'
    PAYOUT_STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (Resolved, 'Resolved'),
        (Closed, 'Closed'),
    ]
    username = models.ForeignKey(User,on_delete=models.CASCADE)
    discord_id = models.TextField()
    ticket_title = models.TextField(default="")
    support_message = models.TextField()
    ticket_status = models.CharField(
        max_length=20,
        choices=PAYOUT_STATUS_CHOICES,
        default=PENDING,
    )
    created_at = models.DateField(auto_now_add=True)
    def __str__(self):
     return f"{self.username}"

class Annoucement(models.Model):
   title = models.TextField(max_length=100)
   annoucement_message = models.TextField()
   created_at = models.DateField(auto_now_add=True)


@receiver(post_save, sender=PayoutRequest)
def handle_completed_payout(sender, instance, **kwargs):
    if instance.payout_status == PayoutRequest.COMPLETED:
        # Get the user's TotalDonation record
        total_donations, created = TotalDonation.objects.get_or_create(username=instance.username)
        
        # Ensure the total donation is not negative after payout
        if total_donations.total_donation >= instance.payout_amount:
            total_donations.total_donation -= instance.payout_amount
            total_donations.save()
        else:
            # Handle cases where payout amount exceeds total donations
            print("Insufficient total donation for payout")

class Alert(models.Model):  # Renamed to Alert for consistency
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    alert_id = models.CharField(max_length=8, unique=True, blank=True)
    alert_image = models.ImageField(upload_to='alerts/',default="alerts/default_donation.gif")
    alert_sound = models.FileField(upload_to='mp3s/', default="mp3s/default_alert_sound.mp3")
    def __str__(self):
        return f"{self.username}"
    def save(self, *args, **kwargs):
        if not self.alert_id:
            while True:
                # Generate a random alert_id
                self.alert_id = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
                # Check for uniqueness
                if not Alert.objects.filter(alert_id=self.alert_id).exists():
                    break
        super().save(*args, **kwargs)

@receiver(post_save, sender=User)
def create_user_alert(sender, instance, created, **kwargs):
    if created:
        Alert.objects.create(username=instance)

class Donation_page(models.Model):
    username = models.ForeignKey(User , on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profiles/',default="profiles/default__user_pfp.jpg")
    page_message = models.TextField(default="")
    
    def __str__(self):
        return f"{self.username}"

@receiver(post_save, sender=User)
def create_user_alert(sender, instance, created, **kwargs):
    if created:
        Donation_page.objects.create(username=instance)

