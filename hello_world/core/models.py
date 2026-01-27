from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator

# System Administration Models
class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    head = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='department_head')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

class Clinic(models.Model):
    name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} - {self.department.name}"

class InsuranceProvider(models.Model):
    name = models.CharField(max_length=100, unique=True)
    address = models.TextField(blank=True)
    phone = models.CharField(max_length=15, blank=True)
    email = models.EmailField(blank=True)
    contact_person = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class MedicalScheme(models.Model):
    name = models.CharField(max_length=100)
    insurance_provider = models.ForeignKey(InsuranceProvider, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    coverage_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.insurance_provider.name})"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    role = models.CharField(max_length=50, choices=[
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
    employee_id = models.CharField(max_length=20, unique=True, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True)
    specialization = models.CharField(max_length=100, blank=True)  # For doctors
    license_number = models.CharField(max_length=50, blank=True)
    date_joined = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.get_role_display()}"

# Patient Register Models
class Patient(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')])
    marital_status = models.CharField(max_length=20, choices=[
        ('single', 'Single'),
        ('married', 'Married'),
        ('divorced', 'Divorced'),
        ('widowed', 'Widowed'),
    ], blank=True)
    phone = models.CharField(max_length=15)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    emergency_contact_name = models.CharField(max_length=100, blank=True)
    emergency_contact_phone = models.CharField(max_length=15, blank=True)
    medical_record_number = models.CharField(max_length=20, unique=True)
    national_id = models.CharField(max_length=20, blank=True)
    insurance_provider = models.ForeignKey(InsuranceProvider, on_delete=models.SET_NULL, null=True, blank=True)
    medical_scheme = models.ForeignKey(MedicalScheme, on_delete=models.SET_NULL, null=True, blank=True)
    registration_date = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)

    @property
    def full_name(self):
        return f"{self.first_name} {self.middle_name} {self.last_name}".strip()

    @property
    def age(self):
        today = timezone.now().date()
        return today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))

    def __str__(self):
        return f"{self.medical_record_number} - {self.full_name}"

class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'userprofile__role': 'doctor'})
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=[
        ('scheduled', 'Scheduled'),
        ('confirmed', 'Confirmed'),
        ('checked_in', 'Checked In'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('no_show', 'No Show'),
    ], default='scheduled')
    appointment_type = models.CharField(max_length=50, choices=[
        ('consultation', 'Consultation'),
        ('follow_up', 'Follow-up'),
        ('procedure', 'Procedure'),
        ('emergency', 'Emergency'),
    ], default='consultation')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.patient} - {self.doctor.get_full_name()} - {self.date}"

# Payment Models
class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    category = models.CharField(max_length=50, choices=[
        ('consultation', 'Consultation'),
        ('laboratory', 'Laboratory'),
        ('radiology', 'Radiology'),
        ('pharmacy', 'Pharmacy'),
        ('procedure', 'Procedure'),
        ('admission', 'Admission'),
    ])
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} - ${self.price}"

class Invoice(models.Model):
    invoice_number = models.CharField(max_length=20, unique=True, default='INV-0000')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    services = models.ManyToManyField(Service, through='InvoiceItem')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    insurance_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=[
        ('draft', 'Draft'),
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('overdue', 'Overdue'),
        ('cancelled', 'Cancelled'),
    ], default='draft')
    payment_method = models.CharField(max_length=20, choices=[
        ('cash', 'Cash'),
        ('card', 'Card'),
        ('bank_transfer', 'Bank Transfer'),
        ('mobile_money', 'Mobile Money'),
        ('insurance', 'Insurance'),
        ('waiver', 'Waiver'),
    ], blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    due_date = models.DateField(null=True, blank=True)

    @property
    def balance(self):
        return self.total_amount - self.paid_amount - self.insurance_amount

    def __str__(self):
        return f"Invoice {self.invoice_number} - {self.patient}"

class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.unit_price
        super().save(*args, **kwargs)

# Laboratory Management Models
class LabTest(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    normal_range = models.CharField(max_length=100, blank=True)
    unit = models.CharField(max_length=50, blank=True)
    category = models.CharField(max_length=50, choices=[
        ('hematology', 'Hematology'),
        ('biochemistry', 'Biochemistry'),
        ('microbiology', 'Microbiology'),
        ('parasitology', 'Parasitology'),
        ('immunology', 'Immunology'),
    ])
    turnaround_time = models.CharField(max_length=50, blank=True)  # e.g., "24 hours"
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class LabRequest(models.Model):
    request_number = models.CharField(max_length=20, unique=True, default='LAB-0000')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(User, on_delete=models.CASCADE)
    tests = models.ManyToManyField(LabTest)
    priority = models.CharField(max_length=20, choices=[
        ('routine', 'Routine'),
        ('urgent', 'Urgent'),
        ('stat', 'STAT'),
    ], default='routine')
    status = models.CharField(max_length=20, choices=[
        ('requested', 'Requested'),
        ('sample_collected', 'Sample Collected'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ], default='requested')
    clinical_info = models.TextField(blank=True)
    requested_at = models.DateTimeField(default=timezone.now)
    completed_at = models.DateTimeField(null=True, blank=True)
    technician = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='lab_technician')

    def __str__(self):
        return f"Lab Request {self.request_number}"

class LabResult(models.Model):
    lab_request = models.ForeignKey(LabRequest, on_delete=models.CASCADE)
    test = models.ForeignKey(LabTest, on_delete=models.CASCADE)
    result = models.CharField(max_length=100)
    reference_range = models.CharField(max_length=100, blank=True)
    flag = models.CharField(max_length=20, choices=[
        ('normal', 'Normal'),
        ('high', 'High'),
        ('low', 'Low'),
        ('critical', 'Critical'),
    ], blank=True)
    notes = models.TextField(blank=True)
    technician = models.ForeignKey(User, on_delete=models.CASCADE)
    verified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='verified_results')
    verified_at = models.DateTimeField(null=True, blank=True)

# Pharmacy Models
class Drug(models.Model):
    name = models.CharField(max_length=100)
    generic_name = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=50)
    strength = models.CharField(max_length=50, blank=True)
    form = models.CharField(max_length=50, choices=[
        ('tablet', 'Tablet'),
        ('capsule', 'Capsule'),
        ('syrup', 'Syrup'),
        ('injection', 'Injection'),
        ('cream', 'Cream'),
        ('ointment', 'Ointment'),
    ], default='tablet')
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    stock_quantity = models.PositiveIntegerField(default=0)
    reorder_level = models.PositiveIntegerField(default=10)
    expiry_date = models.DateField(null=True, blank=True)
    manufacturer = models.CharField(max_length=100, blank=True)
    batch_number = models.CharField(max_length=50, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} {self.strength}"

class Prescription(models.Model):
    prescription_number = models.CharField(max_length=20, unique=True, default='RX-0000')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(User, on_delete=models.CASCADE)
    drugs = models.ManyToManyField(Drug, through='PrescriptionItem')
    diagnosis = models.TextField(blank=True)
    instructions = models.TextField(blank=True)
    prescribed_at = models.DateTimeField(default=timezone.now)
    dispensed_at = models.DateTimeField(null=True, blank=True)
    dispensed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='dispensed_prescriptions')

    def __str__(self):
        return f"Prescription {self.prescription_number}"

class PrescriptionItem(models.Model):
    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE)
    drug = models.ForeignKey(Drug, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    dosage = models.CharField(max_length=100)
    frequency = models.CharField(max_length=100)
    duration = models.CharField(max_length=50)
    instructions = models.TextField(blank=True)

# Out Patient Models
class OutPatientVisit(models.Model):
    visit_number = models.CharField(max_length=20, unique=True, default='VIS-0000')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(User, on_delete=models.CASCADE)
    appointment = models.OneToOneField(Appointment, on_delete=models.SET_NULL, null=True, blank=True)
    chief_complaint = models.TextField()
    history_of_present_illness = models.TextField(verbose_name="HPI")
    past_medical_history = models.TextField(blank=True)
    physical_examination = models.TextField()
    assessment = models.TextField()
    diagnosis = models.TextField()
    treatment_plan = models.TextField()
    prescriptions = models.ManyToManyField(Prescription, blank=True)
    lab_requests = models.ManyToManyField(LabRequest, blank=True)
    follow_up_date = models.DateField(null=True, blank=True)
    visit_date = models.DateTimeField(default=timezone.now)
    next_visit_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Visit {self.visit_number} - {self.patient}"

# Nursing Models
class VitalSigns(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    nurse = models.ForeignKey(User, on_delete=models.CASCADE)
    temperature = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    temperature_unit = models.CharField(max_length=5, choices=[('C', 'Celsius'), ('F', 'Fahrenheit')], default='C')
    blood_pressure_systolic = models.PositiveIntegerField(null=True, blank=True)
    blood_pressure_diastolic = models.PositiveIntegerField(null=True, blank=True)
    heart_rate = models.PositiveIntegerField(null=True, blank=True)
    respiratory_rate = models.PositiveIntegerField(null=True, blank=True)
    oxygen_saturation = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    height = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    bmi = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    recorded_at = models.DateTimeField(default=timezone.now)

    @property
    def blood_pressure(self):
        if self.blood_pressure_systolic and self.blood_pressure_diastolic:
            return f"{self.blood_pressure_systolic}/{self.blood_pressure_diastolic}"
        return None

class NursingNote(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    nurse = models.ForeignKey(User, on_delete=models.CASCADE)
    note_type = models.CharField(max_length=50, choices=[
        ('assessment', 'Assessment'),
        ('intervention', 'Intervention'),
        ('progress', 'Progress Note'),
        ('discharge', 'Discharge Note'),
    ])
    note = models.TextField()
    recorded_at = models.DateTimeField(default=timezone.now)

# Inventory Management Models
class Supplier(models.Model):
    name = models.CharField(max_length=100, unique=True)
    address = models.TextField(blank=True)
    phone = models.CharField(max_length=15, blank=True)
    email = models.EmailField(blank=True)
    contact_person = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class InventoryItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=50, choices=[
        ('medicine', 'Medicine'),
        ('medical_supply', 'Medical Supply'),
        ('equipment', 'Equipment'),
        ('consumable', 'Consumable'),
    ])
    unit = models.CharField(max_length=20, default='pieces')
    quantity = models.PositiveIntegerField(default=0)
    reorder_level = models.PositiveIntegerField(default=10)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True)
    batch_number = models.CharField(max_length=50, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)

    @property
    def total_value(self):
        return self.quantity * self.unit_price

    def __str__(self):
        return f"{self.name} ({self.quantity} {self.unit})"

# Basic models for other modules - can be expanded
class RadiologyRequest(models.Model):
    request_number = models.CharField(max_length=20, unique=True, default='RAD-0000')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(User, on_delete=models.CASCADE)
    examination_type = models.CharField(max_length=100)
    clinical_info = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=[
        ('requested', 'Requested'),
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ], default='requested')
    requested_at = models.DateTimeField(default=timezone.now)

class InPatientAdmission(models.Model):
    admission_number = models.CharField(max_length=20, unique=True, default='ADM-0000')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    admitting_doctor = models.ForeignKey(User, on_delete=models.CASCADE)
    ward = models.CharField(max_length=50)
    bed_number = models.CharField(max_length=10)
    admission_date = models.DateTimeField(default=timezone.now)
    discharge_date = models.DateTimeField(null=True, blank=True)
    diagnosis = models.TextField()
    status = models.CharField(max_length=20, choices=[
        ('admitted', 'Admitted'),
        ('discharged', 'Discharged'),
        ('transferred', 'Transferred'),
    ], default='admitted')

# Human Resources Models
class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    employee_id = models.CharField(max_length=20, unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=100)
    employment_type = models.CharField(max_length=20, choices=[
        ('permanent', 'Permanent'),
        ('contract', 'Contract'),
        ('part_time', 'Part Time'),
    ])
    hire_date = models.DateField()
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.employee_id}"

class Payroll(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    period_start = models.DateField()
    period_end = models.DateField()
    basic_salary = models.DecimalField(max_digits=10, decimal_places=2)
    allowances = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    deductions = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    net_pay = models.DecimalField(max_digits=10, decimal_places=2)
    processed_at = models.DateTimeField(default=timezone.now)

# Asset Register Models
class Asset(models.Model):
    asset_tag = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    purchase_date = models.DateField()
    purchase_cost = models.DecimalField(max_digits=10, decimal_places=2)
    current_value = models.DecimalField(max_digits=10, decimal_places=2)
    depreciation_rate = models.DecimalField(max_digits=5, decimal_places=2)
    location = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.asset_tag} - {self.name}"