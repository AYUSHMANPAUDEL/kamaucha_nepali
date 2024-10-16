from django.contrib import admin
from home.models import Donation , TotalDonation , PayoutRequest

# Register your models here.
admin.site.register(Donation)
admin.site.register(TotalDonation)
admin.site.register(PayoutRequest)

