from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Notification

class NotificationService:
    """
    Service for managing real-time notifications
    """

    @staticmethod
    def send_notification_to_user(user_id, data):
        """
        Send notification to specific user via WebSocket
        """
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'notifications_{user_id}',
            {
                'type': 'send_notification',
                'data': data
            }
        )

    @staticmethod
    def send_notification_to_group(group_name, data):
        """
        Send notification to a group via WebSocket
        """
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                'type': 'send_notification',
                'data': data
            }
        )

    @staticmethod
    def create_and_send_notification(recipient, title, message, notification_type='info',
                                   priority='medium', sender=None, **kwargs):
        """
        Create a notification and send it in real-time
        """
        # Create notification in database
        notification = Notification.objects.create(
            recipient=recipient,
            sender=sender,
            title=title,
            message=message,
            notification_type=notification_type,
            priority=priority,
            **kwargs
        )

        # Prepare data for WebSocket
        notification_data = {
            'id': notification.id,
            'title': notification.title,
            'message': notification.message,
            'type': notification.notification_type,
            'priority': notification.priority,
            'created_at': notification.created_at.isoformat(),
            'action_url': notification.action_url or '',
            'action_text': notification.action_text or '',
        }

        # Send via WebSocket
        NotificationService.send_notification_to_user(recipient.id, notification_data)

        return notification

    @staticmethod
    def notify_doctors_new_wound_case(wound_case):
        """
        Notify all doctors about new wound case
        """
        from .models import UserProfile

        doctors = UserProfile.objects.filter(role='doctor').select_related('user')
        for doctor_profile in doctors:
            NotificationService.create_and_send_notification(
                recipient=doctor_profile.user,
                title=f'New Wound Case: {wound_case.wound_id}',
                message=f'Patient: {wound_case.patient.full_name} - {wound_case.wound_type.name}',
                notification_type='wound_care',
                priority='high',
                related_wound=wound_case,
                action_url=f'/core/wounds/{wound_case.id}/',
                action_text='View Case'
            )

    @staticmethod
    def notify_patient_appointment_reminder(appointment):
        """
        Send appointment reminder to patient
        """
        # In a real system, you'd have patient notification preferences
        # For now, we'll notify the user who created the appointment
        NotificationService.create_and_send_notification(
            recipient=appointment.doctor,
            title=f'Appointment Reminder: {appointment.patient.full_name}',
            message=f'Scheduled for {appointment.date.strftime("%B %d, %Y at %I:%M %p")}',
            notification_type='appointment',
            priority='medium',
            related_appointment=appointment,
            action_url=f'/core/appointments/{appointment.id}/',
            action_text='View Details'
        )

    @staticmethod
    def notify_lab_results_ready(lab_request):
        """
        Notify relevant staff about completed lab results
        """
        from .models import UserProfile

        # Notify doctors and lab techs
        medical_staff = UserProfile.objects.filter(
            role__in=['doctor', 'lab_tech']
        ).select_related('user')

        for staff_profile in medical_staff:
            NotificationService.create_and_send_notification(
                recipient=staff_profile.user,
                title=f'Lab Results Ready: {lab_request.patient.full_name}',
                message=f'{lab_request.tests} results are now available',
                notification_type='lab_result',
                priority='high',
                related_patient=lab_request.patient,
                action_url=f'/core/lab/requests/{lab_request.id}/',
                action_text='View Results'
            )

    @staticmethod
    def notify_billing_update(billing):
        """
        Notify about billing updates
        """
        from .models import UserProfile

        # Notify cashiers and admins
        finance_staff = UserProfile.objects.filter(
            role__in=['cashier', 'admin', 'super_admin']
        ).select_related('user')

        for staff_profile in finance_staff:
            NotificationService.create_and_send_notification(
                recipient=staff_profile.user,
                title=f'Billing Update: {billing.wound.wound_id}',
                message=f'Payment status: {billing.get_payment_status_display()} - Balance: ${billing.balance}',
                notification_type='billing',
                priority='medium' if billing.balance > 0 else 'high',
                action_url=f'/core/wounds/{billing.wound.id}/billing/',
                action_text='View Billing'
            )

    @staticmethod
    def broadcast_system_notification(title, message, user_roles=None):
        """
        Send system-wide notification to specific roles
        """
        from .models import UserProfile

        if user_roles:
            recipients = UserProfile.objects.filter(role__in=user_roles).select_related('user')
        else:
            recipients = UserProfile.objects.all().select_related('user')

        for profile in recipients:
            NotificationService.create_and_send_notification(
                recipient=profile.user,
                title=title,
                message=message,
                notification_type='system',
                priority='medium'
            )

class AuditService:
    """
    Service for audit logging and compliance
    """

    @staticmethod
    def log_user_action(user, action, object_type, object_id, details=None, ip_address=None):
        """
        Log user actions for audit trail
        """
        from auditlog.models import LogEntry
        from django.contrib.contenttypes.models import ContentType

        try:
            content_type = ContentType.objects.get(model=object_type.lower())
            LogEntry.objects.create(
                actor=user,
                content_type=content_type,
                object_id=object_id,
                object_repr=str(details) if details else '',
                action=action,  # 0=CREATE, 1=UPDATE, 2=DELETE
                changes=str(details) if details else '',
                remote_addr=ip_address,
            )
        except Exception as e:
            # Log audit failure but don't break the main flow
            print(f"Audit logging failed: {e}")

    @staticmethod
    def get_audit_trail(model_name, object_id, days=30):
        """
        Get audit trail for an object
        """
        from auditlog.models import LogEntry
        from django.contrib.contenttypes.models import ContentType
        from django.utils import timezone

        try:
            content_type = ContentType.objects.get(model=model_name.lower())
            since_date = timezone.now() - timezone.timedelta(days=days)

            return LogEntry.objects.filter(
                content_type=content_type,
                object_id=object_id,
                timestamp__gte=since_date
            ).order_by('-timestamp')
        except ContentType.DoesNotExist:
            return LogEntry.objects.none()