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


# ==================== WOUND CARE MANAGEMENT SYSTEM ====================
# Professional integrated wound care system for all staff

class WoundType(models.Model):
    """Classification of wound types"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=50, choices=[
        ('acute', 'Acute Wound'),
        ('chronic', 'Chronic Wound'),
        ('surgical', 'Surgical Wound'),
        ('trauma', 'Trauma Wound'),
        ('burn', 'Burn Wound'),
        ('ulcer', 'Pressure/Leg Ulcer'),
        ('diabetic', 'Diabetic Ulcer'),
    ])
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class BodyPart(models.Model):
    """Body parts for wound location"""
    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=50, choices=[
        ('head', 'Head/Face'),
        ('trunk', 'Trunk'),
        ('upper_limb', 'Upper Limb'),
        ('lower_limb', 'Lower Limb'),
        ('other', 'Other'),
    ])
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class WoundCare(models.Model):
    """Main wound care assessment and tracking"""
    WOUND_STATUS_CHOICES = [
        ('active', 'Active Case'),
        ('pending', 'Pending Treatment'),
        ('healing', 'Healing'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ]
    
    # Identification
    wound_id = models.CharField(max_length=20, unique=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='wound_cases')
    
    # Assessment Info
    assessment_date = models.DateTimeField(default=timezone.now)
    assessed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='wound_assessments')
    
    # Wound Details
    wound_type = models.ForeignKey(WoundType, on_delete=models.SET_NULL, null=True)
    body_part = models.ForeignKey(BodyPart, on_delete=models.SET_NULL, null=True)
    laterality = models.CharField(max_length=20, choices=[
        ('left', 'Left'),
        ('right', 'Right'),
        ('bilateral', 'Bilateral'),
        ('midline', 'Midline'),
    ], blank=True)
    
    # Wound Measurements
    length_cm = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, help_text="Length in cm")
    width_cm = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, help_text="Width in cm")
    depth_cm = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, help_text="Depth in cm")
    surface_area_cm2 = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True, help_text="Surface area in cm²")
    
    # Clinical Assessment
    appearance = models.TextField(blank=True, help_text="Describe wound appearance, color, etc.")
    exudate = models.CharField(max_length=50, choices=[
        ('none', 'No exudate'),
        ('serous', 'Serous (clear/straw)'),
        ('seropurulent', 'Seropurulent (cloudy/yellow)'),
        ('purulent', 'Purulent (thick/yellow-green)'),
        ('sanguineous', 'Sanguineous (blood)'),
    ], blank=True)
    exudate_amount = models.CharField(max_length=20, choices=[
        ('minimal', 'Minimal'),
        ('moderate', 'Moderate'),
        ('heavy', 'Heavy'),
    ], blank=True)
    
    # Pain and Edema
    pain_level = models.IntegerField(default=0, validators=[MinValueValidator(0)])  # 0-10 scale
    has_edema = models.BooleanField(default=False)
    edema_grade = models.CharField(max_length=20, choices=[
        ('none', 'None'),
        ('mild', 'Mild 1+'),
        ('moderate', 'Moderate 2+'),
        ('severe', 'Severe 3+'),
        ('pitting', 'Pitting 4+'),
    ], blank=True)
    
    # Infection Status
    signs_of_infection = models.BooleanField(default=False)
    infection_notes = models.TextField(blank=True)
    
    # Insurance & Billing
    patient_insurance = models.ForeignKey(InsuranceProvider, on_delete=models.SET_NULL, null=True, blank=True)
    insurance_covers = models.BooleanField(default=False)
    copay_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0, help_text="Patient's copay %")
    
    # Status Tracking
    status = models.CharField(max_length=20, choices=WOUND_STATUS_CHOICES, default='active')
    next_visit_date = models.DateField(blank=True, null=True)
    
    # Notes & History
    clinical_notes = models.TextField(blank=True)
    treatment_plan = models.TextField(blank=True)
    
    # System Fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-assessment_date']
        indexes = [
            models.Index(fields=['patient', 'status']),
            models.Index(fields=['assessment_date']),
        ]

    def __str__(self):
        return f"Wound #{self.wound_id} - {self.patient.full_name} - {self.get_status_display()}"
    
    def save(self, *args, **kwargs):
        """Auto-calculate surface area if length and width are provided"""
        if self.length_cm and self.width_cm and not self.surface_area_cm2:
            self.surface_area_cm2 = self.length_cm * self.width_cm
        super().save(*args, **kwargs)


class WoundTreatment(models.Model):
    """Wound care treatment procedures and interventions"""
    wound = models.ForeignKey(WoundCare, on_delete=models.CASCADE, related_name='treatments')
    treatment_date = models.DateTimeField(default=timezone.now)
    performed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    # Treatment Details
    treatment_type = models.CharField(max_length=100, choices=[
        ('dressing_change', 'Dressing Change'),
        ('debridement', 'Debridement'),
        ('wound_wash', 'Wound Wash/Irrigation'),
        ('antiseptic', 'Antiseptic/Antibiotic Application'),
        ('compression', 'Compression Therapy'),
        ('vacuum_therapy', 'Negative Pressure (VAC) Therapy'),
        ('medication', 'Medication Application'),
        ('cultures', 'Wound Culture/Sample'),
        ('other', 'Other Procedure'),
    ])
    
    description = models.TextField(help_text="Detailed description of treatment performed")
    materials_used = models.TextField(blank=True, help_text="Dressings, antiseptics, gauze, etc.")
    
    # Post-Treatment Assessment
    pain_after = models.IntegerField(default=0, validators=[MinValueValidator(0)], help_text="Pain level after (0-10)")
    bleeding = models.BooleanField(default=False)
    complications = models.TextField(blank=True)
    
    # Notes for Next Visit
    instructions = models.TextField(blank=True, help_text="Home care instructions for patient")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-treatment_date']

    def __str__(self):
        return f"{self.get_treatment_type_display()} - {self.wound.wound_id} ({self.treatment_date.date()})"


class WoundBilling(models.Model):
    """Billing integration for wound care services"""
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending Payment'),
        ('partial', 'Partially Paid'),
        ('paid', 'Fully Paid'),
        ('waived', 'Waived/Free'),
    ]
    
    wound = models.OneToOneField(WoundCare, on_delete=models.CASCADE, related_name='billing')
    billing_date = models.DateTimeField(default=timezone.now)
    
    # Service Charges
    assessment_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    treatment_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    dressing_supplies_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    medication_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    other_charges = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Insurance & Payment
    insurance_covers = models.BooleanField(default=False)
    insurance_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    patient_copay = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Payment Tracking
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50, choices=[
        ('cash', 'Cash'),
        ('card', 'Card'),
        ('check', 'Check'),
        ('mobile_money', 'Mobile Money'),
        ('insurance', 'Insurance'),
        ('waived', 'Waived'),
    ], blank=True)
    payment_date = models.DateField(blank=True, null=True)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    
    # Tracking
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Invoice #{self.id} - {self.wound.wound_id} - {self.get_payment_status_display()}"
    
    def save(self, *args, **kwargs):
        """Auto-calculate totals"""
        self.total_amount = (self.assessment_fee + self.treatment_fee + 
                            self.dressing_supplies_cost + self.medication_cost + 
                            self.other_charges)
        self.balance = self.total_amount - self.amount_paid
        super().save(*args, **kwargs)


class WoundFollowUp(models.Model):
    """Follow-up visits and progress tracking"""
    wound = models.ForeignKey(WoundCare, on_delete=models.CASCADE, related_name='follow_ups')
    followup_date = models.DateTimeField(default=timezone.now)
    conducted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    # Progress Assessment
    wound_status = models.CharField(max_length=20, choices=[
        ('improving', 'Improving'),
        ('stable', 'Stable'),
        ('deteriorating', 'Deteriorating'),
        ('resolved', 'Resolved'),
    ])
    
    # Updated Measurements
    length_cm = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    width_cm = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    depth_cm = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    
    # Assessment
    appearance_notes = models.TextField(blank=True)
    pain_level = models.IntegerField(default=0)
    signs_of_infection = models.BooleanField(default=False)
    
    # Treatment Adjustment
    treatment_adjusted = models.BooleanField(default=False)
    adjustment_reason = models.TextField(blank=True)
    
    # Next Steps
    next_followup_date = models.DateField(blank=True, null=True)
    notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-followup_date']

    def __str__(self):
        return f"Follow-up - {self.wound.wound_id} ({self.followup_date.date()})"


class PaymentTransaction(models.Model):
    """Track individual payment transactions for wound billing"""
    TRANSACTION_STATUS = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'),
    ]
    
    # Kenya-specific payment methods
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('mpesa', 'M-Pesa'),
        ('airtel_money', 'Airtel Money'),
        ('equity_bank', 'Equity Bank'),
        ('kcb_bank', 'KCB Bank'),
        ('co_op_bank', 'Co-op Bank'),
        ('other_bank', 'Other Bank Transfer'),
        ('card_visa', 'Visa Card'),
        ('card_mastercard', 'Mastercard'),
        ('card_debit', 'Debit Card'),
        ('insurance_claim', 'Insurance Claim Payment'),
        ('employer_scheme', 'Employer/Corporate Scheme'),
        ('credit_account', 'Hospital Credit Account'),
    ]
    
    billing = models.ForeignKey(WoundBilling, on_delete=models.CASCADE, related_name='transactions')
    transaction_ref = models.CharField(max_length=50, unique=True)
    
    # Payment Details
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHOD_CHOICES)
    
    # Mobile Money Specific (M-Pesa, Airtel, etc.)
    mpesa_phone = models.CharField(max_length=15, blank=True, help_text="M-Pesa phone number")
    mpesa_receipt = models.CharField(max_length=20, blank=True, help_text="M-Pesa STK confirmation code")
    
    # Bank Transfer Specific
    bank_name = models.CharField(max_length=100, blank=True)
    bank_account = models.CharField(max_length=30, blank=True)
    cheque_number = models.CharField(max_length=20, blank=True)
    
    # Card Payment Specific
    card_last4 = models.CharField(max_length=4, blank=True, help_text="Last 4 digits of card")
    card_reference = models.CharField(max_length=50, blank=True, help_text="Card processor reference")
    
    # Transaction Status
    status = models.CharField(max_length=20, choices=TRANSACTION_STATUS, default='completed')
    transaction_date = models.DateTimeField(default=timezone.now)
    
    # Verification & Receipt
    receipt_number = models.CharField(max_length=50, blank=True, unique=True)
    is_verified = models.BooleanField(default=False, help_text="Payment verified/confirmed")
    verification_date = models.DateTimeField(blank=True, null=True)
    
    # Notes
    notes = models.TextField(blank=True)
    processed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Refund Tracking
    refund_ref = models.CharField(max_length=50, blank=True, unique=True)
    refund_date = models.DateTimeField(blank=True, null=True)
    refund_reason = models.TextField(blank=True)
    
    # Tracking
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-transaction_date']
        indexes = [
            models.Index(fields=['billing', 'transaction_date']),
            models.Index(fields=['payment_method', 'status']),
            models.Index(fields=['mpesa_phone', 'transaction_date']),
        ]
    
    def __str__(self):
        return f"{self.transaction_ref} - KES {self.amount} ({self.get_payment_method_display()})"


class InsuranceClaim(models.Model):
    """Track insurance claims for wound care services"""
    CLAIM_STATUS = [
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('under_review', 'Under Review'),
        ('approved', 'Approved'),
        ('approved_partial', 'Approved - Partial'),
        ('rejected', 'Rejected'),
        ('paid', 'Paid'),
    ]
    
    billing = models.OneToOneField(WoundBilling, on_delete=models.CASCADE, related_name='insurance_claim')
    claim_number = models.CharField(max_length=50, unique=True)
    
    # Claim Details
    submitted_date = models.DateTimeField(blank=True, null=True)
    claim_amount = models.DecimalField(max_digits=10, decimal_places=2)
    insurance_provider = models.ForeignKey(InsuranceProvider, on_delete=models.SET_NULL, null=True)
    medical_scheme = models.ForeignKey(MedicalScheme, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Approval Details
    approval_date = models.DateTimeField(blank=True, null=True)
    approved_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    approval_notes = models.TextField(blank=True)
    claim_status = models.CharField(max_length=20, choices=CLAIM_STATUS, default='draft')
    
    # Payment
    paid_date = models.DateTimeField(blank=True, null=True)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Documents & Notes
    claim_documents = models.TextField(blank=True, help_text="List of attached documents")
    submission_notes = models.TextField(blank=True)
    
    # Tracking
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-submitted_date']
        indexes = [
            models.Index(fields=['insurance_provider', 'claim_status']),
        ]
    
    def __str__(self):
        return f"Claim #{self.claim_number} - {self.billing.wound.wound_id} ({self.get_claim_status_display()})"


class PatientBillingAccount(models.Model):
    """Hospital credit account for patients in Kenya"""
    ACCOUNT_STATUS = [
        ('active', 'Active'),
        ('suspended', 'Suspended'),
        ('closed', 'Closed'),
        ('dormant', 'Dormant'),
    ]
    
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE, related_name='billing_account')
    account_number = models.CharField(max_length=20, unique=True)
    
    # Account Details
    credit_limit = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="Maximum credit allowed")
    current_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="Current outstanding balance")
    available_credit = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="Available credit remaining")
    
    # Payment Terms
    payment_terms_days = models.IntegerField(default=30, help_text="Days allowed for payment")
    
    # Account Status
    status = models.CharField(max_length=20, choices=ACCOUNT_STATUS, default='active')
    is_verified = models.BooleanField(default=False, help_text="Account verified by finance")
    
    # Employer/Corporate Scheme
    employer_name = models.CharField(max_length=200, blank=True)
    employer_contact = models.CharField(max_length=100, blank=True)
    employer_reference = models.CharField(max_length=50, blank=True)
    
    # Tracking
    created_at = models.DateTimeField(auto_now_add=True)
    last_payment_date = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['patient', 'status']),
            models.Index(fields=['account_number']),
        ]
    
    def __str__(self):
        return f"Account {self.account_number} - {self.patient.full_name}"
    
    def save(self, *args, **kwargs):
        """Update available credit"""
        self.available_credit = self.credit_limit - self.current_balance
        super().save(*args, **kwargs)


class CreditAccountTransaction(models.Model):
    """Track transactions on patient credit accounts"""
    TRANSACTION_TYPE = [
        ('charge', 'Service Charge'),
        ('payment', 'Payment Received'),
        ('credit', 'Credit Adjustment'),
        ('waiver', 'Amount Waived'),
    ]
    
    account = models.ForeignKey(PatientBillingAccount, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPE)
    
    # Transaction Details
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=200)
    transaction_date = models.DateTimeField(default=timezone.now)
    
    # Related Billing
    wound_billing = models.ForeignKey(WoundBilling, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Balance After Transaction
    balance_before = models.DecimalField(max_digits=10, decimal_places=2)
    balance_after = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Approval
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    approval_notes = models.TextField(blank=True)
    
    # Tracking
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-transaction_date']
    
    def __str__(self):
        return f"{self.get_transaction_type_display()} - {self.account.account_number} - KES {self.amount}"


class CorporatePaymentScheme(models.Model):
    """Manage corporate/employer payment schemes"""
    PAYMENT_FREQUENCY = [
        ('weekly', 'Weekly'),
        ('biweekly', 'Bi-weekly'),
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('annual', 'Annual'),
    ]
    
    SCHEME_STATUS = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('suspended', 'Suspended'),
    ]
    
    name = models.CharField(max_length=200, unique=True)
    employer = models.ForeignKey(InsuranceProvider, on_delete=models.CASCADE, related_name='corporate_schemes')
    
    # Scheme Details
    description = models.TextField(blank=True)
    coverage_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=100)
    maximum_coverage_per_patient = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    
    # Payment Terms
    payment_frequency = models.CharField(max_length=20, choices=PAYMENT_FREQUENCY, default='monthly')
    days_to_pay = models.IntegerField(default=30, help_text="Days allowed before payment is due")
    
    # Contacts
    primary_contact_name = models.CharField(max_length=100, blank=True)
    primary_contact_phone = models.CharField(max_length=15, blank=True)
    primary_contact_email = models.EmailField(blank=True)
    
    billing_contact_name = models.CharField(max_length=100, blank=True)
    billing_contact_phone = models.CharField(max_length=15, blank=True)
    billing_contact_email = models.EmailField(blank=True)
    
    # Bank Details for Payments
    bank_name = models.CharField(max_length=100, blank=True)
    bank_account_number = models.CharField(max_length=30, blank=True)
    bank_branch = models.CharField(max_length=100, blank=True)
    
    # Status
    status = models.CharField(max_length=20, choices=SCHEME_STATUS, default='active')
    
    # Tracking
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.employer.name})"