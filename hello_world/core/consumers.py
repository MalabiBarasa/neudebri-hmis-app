import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from .models import Notification, WoundCare, Appointment
from django.utils import timezone

class NotificationConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer for real-time notifications
    """

    async def connect(self):
        self.user = self.scope['user']
        if self.user.is_authenticated:
            self.room_group_name = f'notifications_{self.user.id}'

            # Join room group
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )

            await self.accept()

            # Send welcome message
            await self.send(text_data=json.dumps({
                'type': 'connection_established',
                'message': 'Connected to notification service',
                'timestamp': timezone.now().isoformat()
            }))

    async def disconnect(self, close_code):
        # Leave room group
        if hasattr(self, 'room_group_name'):
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )

    async def receive(self, text_data):
        """
        Receive message from WebSocket
        """
        text_data_json = json.loads(text_data)
        message_type = text_data_json.get('type', 'message')

        if message_type == 'mark_read':
            notification_id = text_data_json.get('notification_id')
            await self.mark_notification_read(notification_id)

    async def mark_notification_read(self, notification_id):
        """
        Mark notification as read
        """
        if notification_id:
            await database_sync_to_async(self._mark_read)(notification_id)

    def _mark_read(self, notification_id):
        """
        Database operation to mark notification as read
        """
        try:
            notification = Notification.objects.get(
                id=notification_id,
                recipient=self.user
            )
            notification.is_read = True
            notification.save()
        except Notification.DoesNotExist:
            pass

    # Notification handlers
    async def send_notification(self, event):
        """
        Send notification to WebSocket
        """
        await self.send(text_data=json.dumps(event['data']))

class WoundCareConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer for wound care updates
    """

    async def connect(self):
        self.user = self.scope['user']
        if self.user.is_authenticated:
            # Join wound care updates group
            await self.channel_layer.group_add(
                'wound_care_updates',
                self.channel_name
            )

            await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            'wound_care_updates',
            self.channel_name
        )

    async def wound_update(self, event):
        """
        Send wound care update to WebSocket
        """
        await self.send(text_data=json.dumps(event['data']))

class AppointmentConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer for appointment updates
    """

    async def connect(self):
        self.user = self.scope['user']
        if self.user.is_authenticated:
            # Join appointment updates group
            await self.channel_layer.group_add(
                'appointment_updates',
                self.channel_name
            )

            await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            'appointment_updates',
            self.channel_name
        )

    async def appointment_update(self, event):
        """
        Send appointment update to WebSocket
        """
        await self.send(text_data=json.dumps(event['data']))