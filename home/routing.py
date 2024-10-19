from django.urls import path
from . import consumers


websocket_urlpatterns =[
  path('ws/alert/<str:userId>/',consumers.alert_consumer.as_asgi()),
]