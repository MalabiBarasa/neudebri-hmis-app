from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    # User-specific notifications
    re_path(r'ws/notifications/$', consumers.NotificationConsumer.as_asgi()),

    # General updates
    re_path(r'ws/wound-updates/$', consumers.WoundCareConsumer.as_asgi()),
    re_path(r'ws/appointment-updates/$', consumers.AppointmentConsumer.as_asgi()),
]