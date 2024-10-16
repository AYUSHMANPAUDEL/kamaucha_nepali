from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
# Create your models here.
class Donation(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    donator_name = models.TextField(max_length=200)
    donation_amount = models.IntegerField()
    donation_date = models.DateField(auto_now_add=True)

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
    payout_status = models.CharField(
        max_length=20,
        choices=PAYOUT_STATUS_CHOICES,
        default=PENDING,
    )
    appeal_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.username}"