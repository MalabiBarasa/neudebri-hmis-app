from django.contrib import admin
from .models import *

# System Administration
@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'head', 'created_at')
    search_fields = ('name',)

@admin.register(Clinic)
class ClinicAdmin(admin.ModelAdmin):
    list_display = ('name', 'department', 'location', 'phone', 'is_active')
    list_filter = ('department', 'is_active')
    search_fields = ('name', 'department__name')

@admin.register(InsuranceProvider)
class InsuranceProviderAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'is_active')
    search_fields = ('name',)

@admin.register(MedicalScheme)
class MedicalSchemeAdmin(admin.ModelAdmin):
    list_display = ('name', 'insurance_provider', 'coverage_percentage', 'is_active')
    list_filter = ('insurance_provider', 'is_active')
    search_fields = ('name', 'insurance_provider__name')

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'department', 'employee_id', 'phone')
    list_filter = ('role', 'department')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'employee_id')

# Patient Register
@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('medical_record_number', 'full_name', 'phone', 'age', 'gender', 'registration_date')
    list_filter = ('gender', 'marital_status', 'is_active', 'registration_date')
    search_fields = ('first_name', 'last_name', 'medical_record_number', 'phone', 'national_id')
    readonly_fields = ('age',)

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'clinic', 'date', 'status', 'appointment_type')
    list_filter = ('status', 'appointment_type', 'clinic', 'date')
    search_fields = ('patient__first_name', 'patient__last_name', 'doctor__username')

# Payment
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'department', 'category', 'price', 'is_active')
    list_filter = ('department', 'category', 'is_active')
    search_fields = ('name', 'department__name')

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'patient', 'total_amount', 'paid_amount', 'balance', 'status', 'created_at')
    list_filter = ('status', 'payment_method', 'created_at')
    search_fields = ('invoice_number', 'patient__first_name', 'patient__last_name')
    readonly_fields = ('balance',)

# Laboratory
@admin.register(LabTest)
class LabTestAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'turnaround_time', 'is_active')
    list_filter = ('category', 'is_active')
    search_fields = ('name',)

@admin.register(LabRequest)
class LabRequestAdmin(admin.ModelAdmin):
    list_display = ('request_number', 'patient', 'doctor', 'priority', 'status', 'requested_at')
    list_filter = ('status', 'priority', 'requested_at')
    search_fields = ('request_number', 'patient__first_name', 'patient__last_name')

@admin.register(LabResult)
class LabResultAdmin(admin.ModelAdmin):
    list_display = ('lab_request', 'test', 'result', 'flag', 'technician', 'verified_at')
    list_filter = ('flag', 'verified_at')
    search_fields = ('lab_request__request_number', 'test__name')

# Pharmacy
@admin.register(Drug)
class DrugAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'form', 'stock_quantity', 'price', 'is_active')
    list_filter = ('category', 'form', 'is_active')
    search_fields = ('name', 'generic_name')

@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ('prescription_number', 'patient', 'doctor', 'prescribed_at', 'dispensed_at')
    list_filter = ('prescribed_at', 'dispensed_at')
    search_fields = ('prescription_number', 'patient__first_name', 'patient__last_name')

# Out Patient
@admin.register(OutPatientVisit)
class OutPatientVisitAdmin(admin.ModelAdmin):
    list_display = ('visit_number', 'patient', 'doctor', 'chief_complaint', 'visit_date')
    list_filter = ('visit_date',)
    search_fields = ('visit_number', 'patient__first_name', 'patient__last_name', 'chief_complaint')

# Nursing
@admin.register(VitalSigns)
class VitalSignsAdmin(admin.ModelAdmin):
    list_display = ('patient', 'nurse', 'temperature', 'blood_pressure', 'heart_rate', 'recorded_at')
    list_filter = ('recorded_at',)
    search_fields = ('patient__first_name', 'patient__last_name')

@admin.register(NursingNote)
class NursingNoteAdmin(admin.ModelAdmin):
    list_display = ('patient', 'nurse', 'note_type', 'recorded_at')
    list_filter = ('note_type', 'recorded_at')
    search_fields = ('patient__first_name', 'patient__last_name', 'note')

# Inventory
@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'is_active')
    search_fields = ('name',)

@admin.register(InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'quantity', 'unit_price', 'total_value', 'supplier')
    list_filter = ('category', 'supplier')
    search_fields = ('name', 'supplier__name')
    readonly_fields = ('total_value',)

# Other modules
@admin.register(RadiologyRequest)
class RadiologyRequestAdmin(admin.ModelAdmin):
    list_display = ('request_number', 'patient', 'doctor', 'examination_type', 'status')
    list_filter = ('status',)
    search_fields = ('request_number', 'patient__first_name', 'patient__last_name')

@admin.register(InPatientAdmission)
class InPatientAdmissionAdmin(admin.ModelAdmin):
    list_display = ('admission_number', 'patient', 'admitting_doctor', 'ward', 'bed_number', 'status')
    list_filter = ('status', 'admission_date')
    search_fields = ('admission_number', 'patient__first_name', 'patient__last_name')

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('user', 'employee_id', 'department', 'job_title', 'employment_type', 'is_active')
    list_filter = ('department', 'employment_type', 'is_active')
    search_fields = ('user__first_name', 'user__last_name', 'employee_id')

@admin.register(Payroll)
class PayrollAdmin(admin.ModelAdmin):
    list_display = ('employee', 'period_start', 'period_end', 'basic_salary', 'net_pay')
    list_filter = ('period_start', 'period_end')
    search_fields = ('employee__user__first_name', 'employee__user__last_name')

@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ('asset_tag', 'name', 'category', 'current_value', 'location', 'is_active')
    list_filter = ('category', 'is_active')
    search_fields = ('asset_tag', 'name')