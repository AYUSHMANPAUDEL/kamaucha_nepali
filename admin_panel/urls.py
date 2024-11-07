
from django.contrib import admin
from django.urls import path , include
from django.conf.urls.static import static
from django.conf import settings
from admin_panel import views
urlpatterns = [
    path("kamaucha-admin",views.admin_login , name="admin_login"),
    path("kamaucha-dashboard",views.admin_dashboard , name="admin_dashboard")
]
