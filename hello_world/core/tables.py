import django_tables2 as tables
from .models import *

class PatientTable(tables.Table):
    full_name = tables.Column(accessor='full_name', verbose_name='Full Name')
    age = tables.Column(accessor='age', verbose_name='Age')

    class Meta:
        model = Patient
        template_name = "django_tables2/bootstrap5.html"
        fields = ('medical_record_number', 'full_name', 'age', 'phone', 'gender', 'registration_date')

class AppointmentTable(tables.Table):
    patient = tables.Column(linkify=True, accessor='patient__full_name')
    doctor = tables.Column(accessor='doctor__get_full_name')
    clinic = tables.Column(accessor='clinic__name')

    class Meta:
        model = Appointment
        template_name = "django_tables2/bootstrap5.html"
        fields = ('patient', 'doctor', 'clinic', 'date', 'status', 'appointment_type')

class LabRequestTable(tables.Table):
    patient = tables.Column(linkify=True, accessor='patient__full_name')
    doctor = tables.Column(accessor='doctor__get_full_name')
    tests_count = tables.Column(verbose_name='Tests', accessor='tests__count')

    class Meta:
        model = LabRequest
        template_name = "django_tables2/bootstrap5.html"
        fields = ('request_number', 'patient', 'doctor', 'priority', 'status', 'requested_at')

class PrescriptionTable(tables.Table):
    patient = tables.Column(linkify=True, accessor='patient__full_name')
    doctor = tables.Column(accessor='doctor__get_full_name')

    class Meta:
        model = Prescription
        template_name = "django_tables2/bootstrap5.html"
        fields = ('prescription_number', 'patient', 'doctor', 'diagnosis', 'prescribed_at', 'dispensed_at')

class OutPatientVisitTable(tables.Table):
    patient = tables.Column(linkify=True, accessor='patient__full_name')
    doctor = tables.Column(accessor='doctor__get_full_name')

    class Meta:
        model = OutPatientVisit
        template_name = "django_tables2/bootstrap5.html"
        fields = ('visit_number', 'patient', 'doctor', 'chief_complaint', 'visit_date')

class VitalSignsTable(tables.Table):
    patient = tables.Column(linkify=True, accessor='patient__full_name')
    nurse = tables.Column(accessor='nurse__get_full_name')
    blood_pressure = tables.Column(accessor='blood_pressure', verbose_name='BP')

    class Meta:
        model = VitalSigns
        template_name = "django_tables2/bootstrap5.html"
        fields = ('patient', 'nurse', 'temperature', 'blood_pressure', 'heart_rate', 'recorded_at')

class ServiceTable(tables.Table):
    department = tables.Column(accessor='department__name')

    class Meta:
        model = Service
        template_name = "django_tables2/bootstrap5.html"
        fields = ('name', 'department', 'category', 'price', 'is_active')

class InvoiceTable(tables.Table):
    patient = tables.Column(accessor='patient__full_name')
    balance = tables.Column(accessor='balance', verbose_name='Balance')

    class Meta:
        model = Invoice
        template_name = "django_tables2/bootstrap5.html"
        fields = ('invoice_number', 'patient', 'total_amount', 'paid_amount', 'balance', 'status', 'created_at')

class LabTestTable(tables.Table):
    class Meta:
        model = LabTest
        template_name = "django_tables2/bootstrap5.html"
        fields = ('name', 'category', 'price', 'turnaround_time', 'is_active')

class DrugTable(tables.Table):
    class Meta:
        model = Drug
        template_name = "django_tables2/bootstrap5.html"
        fields = ('name', 'category', 'form', 'stock_quantity', 'price', 'is_active')

class InventoryItemTable(tables.Table):
    supplier = tables.Column(accessor='supplier__name')
    total_value = tables.Column(accessor='total_value', verbose_name='Total Value')

    class Meta:
        model = InventoryItem
        template_name = "django_tables2/bootstrap5.html"
        fields = ('name', 'category', 'quantity', 'unit_price', 'total_value', 'supplier', 'is_active')