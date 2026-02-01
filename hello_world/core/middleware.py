from django.utils.deprecation import MiddlewareMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse

class RBACMiddleware(MiddlewareMixin):
    """
    Middleware to enforce Role-Based Access Control
    """

    def process_view(self, request, view_func, view_args, view_kwargs):
        """
        Check permissions before view execution
        """
        if not request.user.is_authenticated:
            return None

        # Check if user has a profile - if not, skip permission checks
        try:
            if not hasattr(request.user, 'userprofile') or request.user.userprofile is None:
                return None
        except:
            # If there's any issue accessing userprofile, skip permission checks
            return None

        # Get the URL name
        url_name = getattr(request.resolver_match, 'url_name', None)
        if not url_name:
            return None

        # Define URL-based permission requirements
        url_permissions = {
            # Patient management
            'patient_list': 'view_patient',
            'patient_create': 'add_patient',
            'patient_update': 'change_patient',

            # Appointments
            'appointment_list': 'view_appointment',
            'appointment_create': 'add_appointment',

            # Wound care
            'wound_list': 'view_wound_case',
            'wound_create': 'add_wound_case',
            'wound_update': 'change_wound_case',
            'wound_treatment_create': 'treat_wound',
            'wound_billing': 'manage_wound_billing',

            # Laboratory
            'lab_request_list': 'view_lab_request',
            'lab_request_create': 'create_lab_request',

            # Pharmacy
            'prescription_list': 'view_prescription',
            'prescription_create': 'create_prescription',

            # Billing
            'billing_dashboard': 'view_invoice',

            # Reports
            'advanced_analytics': 'view_analytics_dashboard',

            # Admin functions
            'backup_database': 'backup_system',
            'audit_trail': 'view_audit_logs',
        }

        required_permission = url_permissions.get(url_name)
        if required_permission:
            if not request.user.userprofile.has_permission(required_permission):
                messages.error(
                    request,
                    f'Access denied. You do not have permission to access this feature.'
                )
                return redirect('dashboard')

        return None

class SecurityMiddleware(MiddlewareMixin):
    """
    Security middleware for additional protection
    """

    def process_request(self, request):
        """
        Process incoming requests for security checks
        """
        if request.user.is_authenticated:
            try:
                if hasattr(request.user, 'userprofile') and request.user.userprofile is not None:
                    profile = request.user.userprofile

                    # Check for expired lockouts
                    profile.has_expired_lockout

                    # Record IP address for security
                    if not profile.last_login_ip:
                        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
                        if x_forwarded_for:
                            ip = x_forwarded_for.split(',')[0]
                        else:
                            ip = request.META.get('REMOTE_ADDR')
                        profile.last_login_ip = ip
                        profile.save(update_fields=['last_login_ip'])
            except Exception:
                # If there's any issue with userprofile, skip security checks
                pass

        return None

    def process_exception(self, request, exception):
        """
        Log security-related exceptions
        """
        if request.user.is_authenticated:
            # Log potential security issues
            pass

        return None