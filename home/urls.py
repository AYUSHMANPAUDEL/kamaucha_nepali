from django.contrib import admin
from django.urls import path , include
from home import views
urlpatterns = [
   path("",views.home_page , name="home_page"),
   path("register/",views.register_page , name="register_page"),
   path("login/", views.login_page , name="login_page"),
   path("dashboard/",views.dashboard_page,name="dashboard_page"),
   path("logout/",views.logout_page,name="logout_page"),
   path("dashboard/support/", views.support_page , name="support_page"),
   path("dashboard/donation_setup_page/", views.donation_page_setup,name="donation_setup_page"),
   path("dashboard/alert_setup_page/", views.alert_setup_page,name="alert_setup_page"),
   path("dashboard/payout_request_page/", views.payout_request_page,name="payout_request_page"),
   path("dashboard/transcations_history_page",views.transcations_history_page,name="transcations_history_page"),
   path("dashboard/donations_page",views.donations_page,name="donations_page"),
   path("alert/<str:alert_id>",views.alert_page , name="alert_page"),
   path("donate/<str:username>",views.donate_page , name="donate_page"),
]
