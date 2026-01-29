from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    role = forms.ChoiceField(choices=[
        ('admin', 'System Administrator'),
        ('doctor', 'Doctor'),
        ('nurse', 'Nurse'),
        ('cashier', 'Cashier'),
        ('lab_tech', 'Laboratory Technician'),
        ('pharmacist', 'Pharmacist'),
        ('receptionist', 'Receptionist'),
        ('radiologist', 'Radiologist'),
        ('hr_manager', 'HR Manager'),
        ('accountant', 'Accountant'),
    ])
    department = forms.ModelChoiceField(queryset=Department.objects.all(), required=False)
    employee_id = forms.CharField(max_length=20, required=False)
    phone = forms.CharField(max_length=15, required=False)
    specialization = forms.CharField(max_length=100, required=False)
    license_number = forms.CharField(max_length=50, required=False)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'role', 'department', 'employee_id', 'phone', 'specialization', 'license_number')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
            UserProfile.objects.create(
                user=user,
                role=self.cleaned_data['role'],
                department=self.cleaned_data.get('department'),
                employee_id=self.cleaned_data.get('employee_id'),
                phone=self.cleaned_data.get('phone'),
                specialization=self.cleaned_data.get('specialization'),
                license_number=self.cleaned_data.get('license_number'),
            )
        return user

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['first_name', 'last_name', 'middle_name', 'date_of_birth', 'gender', 'marital_status',
                 'phone', 'email', 'address', 'emergency_contact_name', 'emergency_contact_phone',
                 'medical_record_number', 'national_id', 'insurance_provider', 'medical_scheme']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['patient', 'doctor', 'clinic', 'date', 'appointment_type', 'notes']
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class LabRequestForm(forms.ModelForm):
    class Meta:
        model = LabRequest
        fields = ['patient', 'doctor', 'tests', 'priority', 'clinical_info']

class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ['patient', 'doctor', 'diagnosis', 'instructions']

class OutPatientVisitForm(forms.ModelForm):
    class Meta:
        model = OutPatientVisit
        fields = ['patient', 'doctor', 'chief_complaint', 'history_of_present_illness',
                 'past_medical_history', 'physical_examination', 'assessment', 'diagnosis',
                 'treatment_plan', 'follow_up_date', 'next_visit_date']

class VitalSignsForm(forms.ModelForm):
    class Meta:
        model = VitalSigns
        fields = ['patient', 'temperature', 'temperature_unit', 'blood_pressure_systolic',
                 'blood_pressure_diastolic', 'heart_rate', 'respiratory_rate', 'oxygen_saturation',
                 'weight', 'height']

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'description', 'head']

class ClinicForm(forms.ModelForm):
    class Meta:
        model = Clinic
        fields = ['name', 'department', 'description', 'location', 'phone', 'is_active']

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'description', 'price', 'department', 'category', 'is_active']

class LabTestForm(forms.ModelForm):
    class Meta:
        model = LabTest
        fields = ['name', 'description', 'price', 'normal_range', 'unit', 'category', 'turnaround_time', 'is_active']

class DrugForm(forms.ModelForm):
    class Meta:
        model = Drug
        fields = ['name', 'generic_name', 'description', 'category', 'strength', 'form',
                 'price', 'stock_quantity', 'reorder_level', 'expiry_date', 'manufacturer',
                 'batch_number', 'is_active']
        widgets = {
            'expiry_date': forms.DateInput(attrs={'type': 'date'}),
        }

class InventoryItemForm(forms.ModelForm):
    class Meta:
        model = InventoryItem
        fields = ['name', 'description', 'category', 'unit', 'quantity', 'reorder_level',
                 'unit_price', 'supplier', 'batch_number', 'expiry_date', 'location', 'is_active']
        widgets = {
            'expiry_date': forms.DateInput(attrs={'type': 'date'}),
        }


# ==================== WOUND CARE FORMS ====================

class WoundCareForm(forms.ModelForm):
    """Form for creating and updating wound assessments"""
    class Meta:
        model = WoundCare
        fields = [
            'patient', 'wound_type', 'body_part', 'laterality',
            'length_cm', 'width_cm', 'depth_cm',
            'appearance', 'exudate', 'exudate_amount', 'pain_level',
            'has_edema', 'edema_grade', 'signs_of_infection', 'infection_notes',
            'patient_insurance', 'insurance_covers', 'copay_percentage',
            'status', 'next_visit_date', 'clinical_notes', 'treatment_plan'
        ]
        widgets = {
            'patient': forms.Select(attrs={'class': 'form-control'}),
            'wound_type': forms.Select(attrs={'class': 'form-control'}),
            'body_part': forms.Select(attrs={'class': 'form-control'}),
            'laterality': forms.Select(attrs={'class': 'form-control'}),
            'length_cm': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'width_cm': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'depth_cm': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'appearance': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'exudate': forms.Select(attrs={'class': 'form-control'}),
            'exudate_amount': forms.Select(attrs={'class': 'form-control'}),
            'pain_level': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'max': '10'}),
            'edema_grade': forms.Select(attrs={'class': 'form-control'}),
            'infection_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'patient_insurance': forms.Select(attrs={'class': 'form-control'}),
            'copay_percentage': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'next_visit_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'clinical_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'treatment_plan': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class WoundTreatmentForm(forms.ModelForm):
    """Form for recording wound treatment procedures"""
    class Meta:
        model = WoundTreatment
        fields = [
            'treatment_type', 'description', 'materials_used',
            'pain_after', 'bleeding', 'complications', 'instructions'
        ]
        widgets = {
            'treatment_type': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'materials_used': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'pain_after': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'max': '10'}),
            'complications': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'instructions': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class WoundFollowUpForm(forms.ModelForm):
    """Form for follow-up visits"""
    class Meta:
        model = WoundFollowUp
        fields = [
            'wound_status', 'length_cm', 'width_cm', 'depth_cm',
            'appearance_notes', 'pain_level', 'signs_of_infection',
            'treatment_adjusted', 'adjustment_reason', 'next_followup_date', 'notes'
        ]
        widgets = {
            'wound_status': forms.Select(attrs={'class': 'form-control'}),
            'length_cm': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'width_cm': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'depth_cm': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'appearance_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'pain_level': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'max': '10'}),
            'adjustment_reason': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'next_followup_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class WoundBillingForm(forms.ModelForm):
    """Form for managing wound billing and payments"""
    class Meta:
        model = WoundBilling
        fields = [
            'assessment_fee', 'treatment_fee', 'dressing_supplies_cost',
            'medication_cost', 'other_charges', 'insurance_covers',
            'insurance_amount', 'patient_copay', 'amount_paid',
            'payment_method', 'payment_date', 'payment_status'
        ]
        widgets = {
            'assessment_fee': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'treatment_fee': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'dressing_supplies_cost': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'medication_cost': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'other_charges': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'insurance_amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'patient_copay': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'amount_paid': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'payment_method': forms.Select(attrs={'class': 'form-control'}),
            'payment_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'payment_status': forms.Select(attrs={'class': 'form-control'}),
        }

class PaymentTransactionForm(forms.ModelForm):
    """Form for recording payment transactions - Kenya optimized"""
    class Meta:
        model = PaymentTransaction
        fields = [
            'amount', 'payment_method', 'mpesa_phone', 'mpesa_receipt',
            'bank_name', 'bank_account', 'cheque_number', 
            'card_last4', 'card_reference', 'receipt_number', 'notes'
        ]
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'KES'}),
            'payment_method': forms.Select(attrs={'class': 'form-control'}),
            'mpesa_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '0712345678'}),
            'mpesa_receipt': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. RFV5ABC123'}),
            'bank_name': forms.TextInput(attrs={'class': 'form-control'}),
            'bank_account': forms.TextInput(attrs={'class': 'form-control'}),
            'cheque_number': forms.TextInput(attrs={'class': 'form-control'}),
            'card_last4': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '4'}),
            'card_reference': forms.TextInput(attrs={'class': 'form-control'}),
            'receipt_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Optional receipt number'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }


class InsuranceClaimForm(forms.ModelForm):
    """Form for managing insurance claims"""
    class Meta:
        model = InsuranceClaim
        fields = [
            'claim_amount', 'insurance_provider', 'medical_scheme',
            'submission_notes', 'claim_documents'
        ]
        widgets = {
            'claim_amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'KES'}),
            'insurance_provider': forms.Select(attrs={'class': 'form-control'}),
            'medical_scheme': forms.Select(attrs={'class': 'form-control'}),
            'submission_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'claim_documents': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'List documents: receipt.pdf, prescription.pdf, etc.'}),
        }


class PatientBillingAccountForm(forms.ModelForm):
    """Form for creating and managing patient billing accounts"""
    class Meta:
        model = PatientBillingAccount
        fields = [
            'patient', 'credit_limit', 'payment_terms_days',
            'employer_name', 'employer_contact', 'employer_reference'
        ]
        widgets = {
            'patient': forms.Select(attrs={'class': 'form-control'}),
            'credit_limit': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'KES'}),
            'payment_terms_days': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'employer_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Optional: Employer name'}),
            'employer_contact': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Optional: Contact info'}),
            'employer_reference': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Optional: Reference code'}),
        }


class CreditAccountTransactionForm(forms.ModelForm):
    """Form for recording credit account transactions"""
    class Meta:
        model = CreditAccountTransaction
        fields = [
            'transaction_type', 'amount', 'description', 'approval_notes'
        ]
        widgets = {
            'transaction_type': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'KES'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'approval_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }


class CorporatePaymentSchemeForm(forms.ModelForm):
    """Form for managing corporate payment schemes"""
    class Meta:
        model = CorporatePaymentScheme
        fields = [
            'name', 'employer', 'coverage_percentage', 'maximum_coverage_per_patient',
            'payment_frequency', 'days_to_pay', 'description',
            'primary_contact_name', 'primary_contact_phone', 'primary_contact_email',
            'billing_contact_name', 'billing_contact_phone', 'billing_contact_email',
            'bank_name', 'bank_account_number', 'bank_branch', 'status'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'employer': forms.Select(attrs={'class': 'form-control'}),
            'coverage_percentage': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0', 'max': '100'}),
            'maximum_coverage_per_patient': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Optional: Maximum per patient'}),
            'payment_frequency': forms.Select(attrs={'class': 'form-control'}),
            'days_to_pay': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'primary_contact_name': forms.TextInput(attrs={'class': 'form-control'}),
            'primary_contact_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+254...'}),
            'primary_contact_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'billing_contact_name': forms.TextInput(attrs={'class': 'form-control'}),
            'billing_contact_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+254...'}),
            'billing_contact_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'bank_name': forms.TextInput(attrs={'class': 'form-control'}),
            'bank_account_number': forms.TextInput(attrs={'class': 'form-control'}),
            'bank_branch': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }
