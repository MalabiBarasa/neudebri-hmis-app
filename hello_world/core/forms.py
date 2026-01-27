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