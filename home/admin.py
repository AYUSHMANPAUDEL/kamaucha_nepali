from django.contrib import admin
from home.models import Donation , TotalDonation , PayoutRequest , Support

# Register your models here.
admin.site.register(Donation)
admin.site.register(TotalDonation)
admin.site.register(PayoutRequest)
admin.site.register(Support)

