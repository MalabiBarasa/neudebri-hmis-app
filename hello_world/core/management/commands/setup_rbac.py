from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Permission, Group
from django.contrib.contenttypes.models import ContentType
from hello_world.core.models import UserProfile, Department
from guardian.shortcuts import assign_perm

class Command(BaseCommand):
    help = 'Setup Role-Based Access Control (RBAC) system with default roles and permissions'

    def handle(self, *args, **options):
        self.stdout.write('Setting up RBAC system...')

        # Create default department if it doesn't exist
        dept, created = Department.objects.get_or_create(
            name='Administration',
            defaults={'description': 'System Administration Department'}
        )

        # Create default roles and assign permissions
        roles_permissions = {
            'super_admin': [
                'view_patient', 'add_patient', 'change_patient', 'delete_patient',
                'view_medical_history', 'add_medical_record', 'emergency_access',
                'view_appointment', 'add_appointment', 'change_appointment',
                'cancel_appointment', 'view_schedule', 'manage_schedule',
                'view_wound_case', 'add_wound_case', 'change_wound_case',
                'treat_wound', 'view_treatment_history', 'manage_wound_billing',
                'view_invoice', 'create_invoice', 'modify_invoice', 'void_invoice',
                'process_payment', 'view_financial_reports', 'manage_insurance',
                'view_lab_request', 'create_lab_request', 'process_lab_results',
                'view_lab_reports', 'manage_lab_inventory',
                'view_prescription', 'create_prescription', 'dispense_medication',
                'view_pharmacy_inventory', 'manage_drug_inventory',
                'view_radiology_request', 'create_radiology_request',
                'process_radiology_results', 'view_imaging_reports',
                'manage_users', 'manage_roles', 'system_configuration',
                'view_audit_logs', 'backup_system', 'restore_system',
                'view_basic_reports', 'view_advanced_reports', 'export_data',
                'view_analytics_dashboard', 'create_custom_reports',
            ],
            'admin': [
                'view_patient', 'add_patient', 'change_patient',
                'view_medical_history', 'add_medical_record',
                'view_appointment', 'add_appointment', 'change_appointment',
                'cancel_appointment', 'view_schedule',
                'view_wound_case', 'add_wound_case', 'change_wound_case',
                'view_invoice', 'create_invoice', 'modify_invoice',
                'process_payment', 'view_financial_reports',
                'view_lab_request', 'create_lab_request',
                'view_prescription', 'create_prescription',
                'manage_users', 'view_audit_logs', 'backup_system',
                'view_basic_reports', 'view_advanced_reports', 'export_data',
            ],
            'doctor': [
                'view_patient', 'add_patient', 'change_patient',
                'view_medical_history', 'add_medical_record', 'emergency_access',
                'view_appointment', 'add_appointment', 'change_appointment',
                'view_schedule', 'manage_schedule',
                'view_wound_case', 'add_wound_case', 'change_wound_case',
                'treat_wound', 'view_treatment_history',
                'view_lab_request', 'create_lab_request',
                'view_prescription', 'create_prescription',
                'view_radiology_request', 'create_radiology_request',
                'view_basic_reports',
            ],
            'nurse': [
                'view_patient', 'change_patient', 'view_medical_history',
                'emergency_access', 'view_appointment', 'change_appointment',
                'view_wound_case', 'add_wound_case', 'change_wound_case',
                'treat_wound', 'view_treatment_history',
                'view_lab_request', 'view_prescription',
                'view_basic_reports',
            ],
            'cashier': [
                'view_patient', 'view_invoice', 'create_invoice',
                'modify_invoice', 'process_payment', 'view_financial_reports',
                'manage_insurance', 'view_basic_reports',
            ],
            'lab_tech': [
                'view_patient', 'view_lab_request', 'create_lab_request',
                'process_lab_results', 'view_lab_reports', 'manage_lab_inventory',
                'view_basic_reports',
            ],
            'pharmacist': [
                'view_patient', 'view_prescription', 'create_prescription',
                'dispense_medication', 'view_pharmacy_inventory',
                'manage_drug_inventory', 'view_basic_reports',
            ],
            'receptionist': [
                'view_patient', 'add_patient', 'change_patient',
                'view_appointment', 'add_appointment', 'change_appointment',
                'cancel_appointment', 'view_schedule',
                'view_basic_reports',
            ],
        }

        # Create groups and assign permissions
        for role, permissions in roles_permissions.items():
            group, created = Group.objects.get_or_create(name=role)
            if created:
                self.stdout.write(f'Created group: {role}')

            # Clear existing permissions
            group.permissions.clear()

            # Add permissions to group
            for perm_codename in permissions:
                try:
                    permission = Permission.objects.filter(codename=perm_codename).first()
                    if permission:
                        group.permissions.add(permission)
                    else:
                        self.stdout.write(
                            self.style.WARNING(f'Permission {perm_codename} not found')
                        )
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f'Error adding permission {perm_codename}: {e}')
                    )

        # Update existing user profiles with new role structure
        self.stdout.write('Updating existing user profiles...')
        for profile in UserProfile.objects.all():
            # Map old roles to new roles
            role_mapping = {
                'admin': 'admin',
                'doctor': 'doctor',
                'nurse': 'nurse',
                'cashier': 'cashier',
                'lab_tech': 'lab_tech',
                'pharmacist': 'pharmacist',
                'receptionist': 'receptionist',
                'radiologist': 'radiologist',
                'hr_manager': 'admin',
                'accountant': 'cashier',
            }

            new_role = role_mapping.get(profile.role, 'guest')
            profile.role = new_role
            profile.save()

            # Add user to corresponding group
            try:
                group = Group.objects.get(name=new_role)
                profile.user.groups.add(group)
                self.stdout.write(f'Added {profile.user.username} to {new_role} group')
            except Group.DoesNotExist:
                self.stdout.write(
                    self.style.WARNING(f'Group {new_role} not found for user {profile.user.username}')
                )

        self.stdout.write(
            self.style.SUCCESS('RBAC system setup completed successfully!')
        )