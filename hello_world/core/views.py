from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django_tables2 import RequestConfig
from .models import *
from .forms import *
from .tables import *

def index(request):
    context = {
        "title": "Sanitas HMIS Lite™ - Neudebri Woundcare Hospital",
    }
    return render(request, "index.html", context)

@login_required
def dashboard(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    context = {
        "title": "Dashboard",
        "user_profile": user_profile,
    }
    return render(request, "dashboard.html", context)

# Patient Register Views
@login_required
def patient_list(request):
    patients = Patient.objects.all()
    table = PatientTable(patients)
    RequestConfig(request).configure(table)
    return render(request, 'patient_list.html', {'table': table})

@login_required
def patient_create(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Patient created successfully.')
            return redirect('patient_list')
    else:
        form = PatientForm()
    return render(request, 'patient_form.html', {'form': form, 'title': 'Add Patient'})

@login_required
def patient_update(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            messages.success(request, 'Patient updated successfully.')
            return redirect('patient_list')
    else:
        form = PatientForm(instance=patient)
    return render(request, 'patient_form.html', {'form': form, 'title': 'Edit Patient'})

@login_required
def appointment_list(request):
    appointments = Appointment.objects.all()
    table = AppointmentTable(appointments)
    RequestConfig(request).configure(table)
    return render(request, 'appointment_list.html', {'table': table})

@login_required
def appointment_create(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Appointment created successfully.')
            return redirect('appointment_list')
    else:
        form = AppointmentForm()
    return render(request, 'appointment_form.html', {'form': form, 'title': 'Schedule Appointment'})

# Laboratory Views
@login_required
def lab_request_list(request):
    requests = LabRequest.objects.all()
    table = LabRequestTable(requests)
    RequestConfig(request).configure(table)
    return render(request, 'lab_request_list.html', {'table': table})

@login_required
def lab_request_create(request):
    if request.method == 'POST':
        form = LabRequestForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Lab request created successfully.')
            return redirect('lab_request_list')
    else:
        form = LabRequestForm()
    return render(request, 'lab_request_form.html', {'form': form, 'title': 'Create Lab Request'})

# Pharmacy Views
@login_required
def prescription_list(request):
    prescriptions = Prescription.objects.all()
    table = PrescriptionTable(prescriptions)
    RequestConfig(request).configure(table)
    return render(request, 'prescription_list.html', {'table': table})

@login_required
def prescription_create(request):
    if request.method == 'POST':
        form = PrescriptionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Prescription created successfully.')
            return redirect('prescription_list')
    else:
        form = PrescriptionForm()
    return render(request, 'prescription_form.html', {'form': form, 'title': 'Create Prescription'})

# Out Patient Views
@login_required
def outpatient_visit_list(request):
    visits = OutPatientVisit.objects.all()
    table = OutPatientVisitTable(visits)
    RequestConfig(request).configure(table)
    return render(request, 'outpatient_visit_list.html', {'table': table})

@login_required
def outpatient_visit_create(request):
    if request.method == 'POST':
        form = OutPatientVisitForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Outpatient visit recorded successfully.')
            return redirect('outpatient_visit_list')
    else:
        form = OutPatientVisitForm()
    return render(request, 'outpatient_visit_form.html', {'form': form, 'title': 'Record Outpatient Visit'})

# Nursing Views
@login_required
def vital_signs_list(request):
    vitals = VitalSigns.objects.all()
    table = VitalSignsTable(vitals)
    RequestConfig(request).configure(table)
    return render(request, 'vital_signs_list.html', {'table': table})

@login_required
def vital_signs_create(request):
    if request.method == 'POST':
        form = VitalSignsForm(request.POST)
        if form.is_valid():
            vital = form.save(commit=False)
            vital.nurse = request.user
            vital.save()
            messages.success(request, 'Vital signs recorded successfully.')
            return redirect('vital_signs_list')
    else:
        form = VitalSignsForm()
    return render(request, 'vital_signs_form.html', {'form': form, 'title': 'Record Vital Signs'})

# ==================== WOUND CARE MANAGEMENT ====================

@login_required
def wound_list(request):
    """List all wound cases with filtering"""
    wounds = WoundCare.objects.filter(is_active=True).select_related(
        'patient', 'assessed_by', 'wound_type', 'body_part', 'patient_insurance'
    )
    
    # Filtering
    status = request.GET.get('status', '')
    patient_id = request.GET.get('patient', '')
    insurance = request.GET.get('insurance', '')
    
    if status:
        wounds = wounds.filter(status=status)
    if patient_id:
        wounds = wounds.filter(patient_id=patient_id)
    if insurance:
        wounds = wounds.filter(insurance_covers=insurance == 'covered')
    
    context = {
        'title': 'Wound Care Cases',
        'wounds': wounds.order_by('-assessment_date'),
        'statuses': WoundCare._meta.get_field('status').choices,
        'patients': Patient.objects.all(),
        'selected_status': status,
        'selected_patient': patient_id,
    }
    return render(request, 'wound_list.html', context)


@login_required
def wound_detail(request, pk):
    """View detailed wound case information"""
    wound = get_object_or_404(WoundCare, pk=pk)
    treatments = wound.treatments.all().order_by('-treatment_date')
    follow_ups = wound.follow_ups.all().order_by('-followup_date')
    
    try:
        billing = wound.billing
    except WoundBilling.DoesNotExist:
        billing = None
    
    context = {
        'title': f'Wound Case {wound.wound_id}',
        'wound': wound,
        'treatments': treatments,
        'follow_ups': follow_ups,
        'billing': billing,
    }
    return render(request, 'wound_detail.html', context)


@login_required
def wound_create(request):
    """Create a new wound case assessment"""
    if request.method == 'POST':
        form = WoundCareForm(request.POST)
        if form.is_valid():
            wound = form.save(commit=False)
            wound.assessed_by = request.user
            
            # Generate wound ID
            last_wound = WoundCare.objects.order_by('-id').first()
            wound_num = (last_wound.id if last_wound else 0) + 1
            wound.wound_id = f"WND-{wound_num:05d}"
            
            wound.save()
            
            # Create billing record
            WoundBilling.objects.create(
                wound=wound,
                insurance_covers=wound.insurance_covers,
                total_amount=0,
                balance=0,
            )
            
            messages.success(request, f'Wound case {wound.wound_id} created successfully.')
            return redirect('wound_detail', pk=wound.pk)
    else:
        form = WoundCareForm()
    
    context = {
        'title': 'Create Wound Assessment',
        'form': form,
    }
    return render(request, 'wound_form.html', context)


@login_required
def wound_update(request, pk):
    """Update wound case assessment"""
    wound = get_object_or_404(WoundCare, pk=pk)
    
    if request.method == 'POST':
        form = WoundCareForm(request.POST, instance=wound)
        if form.is_valid():
            form.save()
            messages.success(request, 'Wound case updated successfully.')
            return redirect('wound_detail', pk=wound.pk)
    else:
        form = WoundCareForm(instance=wound)
    
    context = {
        'title': f'Update Wound Case {wound.wound_id}',
        'form': form,
        'wound': wound,
    }
    return render(request, 'wound_form.html', context)


@login_required
def wound_treatment_create(request, wound_id):
    """Record a treatment procedure for a wound"""
    wound = get_object_or_404(WoundCare, pk=wound_id)
    
    if request.method == 'POST':
        form = WoundTreatmentForm(request.POST)
        if form.is_valid():
            treatment = form.save(commit=False)
            treatment.wound = wound
            treatment.performed_by = request.user
            treatment.save()
            
            messages.success(request, 'Treatment recorded successfully.')
            return redirect('wound_detail', pk=wound.pk)
    else:
        form = WoundTreatmentForm()
    
    context = {
        'title': f'Record Treatment - {wound.wound_id}',
        'form': form,
        'wound': wound,
    }
    return render(request, 'wound_treatment_form.html', context)


@login_required
def wound_followup_create(request, wound_id):
    """Record a follow-up visit"""
    wound = get_object_or_404(WoundCare, pk=wound_id)
    
    if request.method == 'POST':
        form = WoundFollowUpForm(request.POST)
        if form.is_valid():
            followup = form.save(commit=False)
            followup.wound = wound
            followup.conducted_by = request.user
            followup.save()
            
            # Update wound status if needed
            if followup.wound_status == 'resolved':
                wound.status = 'resolved'
                wound.save()
            
            messages.success(request, 'Follow-up visit recorded successfully.')
            return redirect('wound_detail', pk=wound.pk)
    else:
        form = WoundFollowUpForm()
    
    context = {
        'title': f'Follow-up Visit - {wound.wound_id}',
        'form': form,
        'wound': wound,
    }
    return render(request, 'wound_followup_form.html', context)


@login_required
def wound_billing(request, wound_id):
    """Manage billing for a wound case"""
    wound = get_object_or_404(WoundCare, pk=wound_id)
    billing = wound.billing
    
    if request.method == 'POST':
        form = WoundBillingForm(request.POST, instance=billing)
        if form.is_valid():
            form.save()
            messages.success(request, 'Billing information updated.')
            return redirect('wound_detail', pk=wound.pk)
    else:
        form = WoundBillingForm(instance=billing)
    
    context = {
        'title': f'Billing - {wound.wound_id}',
        'form': form,
        'wound': wound,
        'billing': billing,
    }
    return render(request, 'wound_billing_form.html', context)


@login_required
def wound_dashboard(request):
    """Wound care dashboard with analytics"""
    total_cases = WoundCare.objects.filter(is_active=True).count()
    active_cases = WoundCare.objects.filter(status='active').count()
    pending_cases = WoundCare.objects.filter(status='pending').count()
    resolved_cases = WoundCare.objects.filter(status='resolved').count()
    
    # Insurance coverage stats
    insured_cases = WoundCare.objects.filter(insurance_covers=True).count()
    uninsured_cases = WoundCare.objects.filter(insurance_covers=False).count()
    
    # Recent cases
    recent_wounds = WoundCare.objects.filter(is_active=True).order_by('-assessment_date')[:10]
    
    # Payment status
    pending_payments = WoundBilling.objects.filter(payment_status='pending').aggregate(
        total=models.Sum('balance')
    )['total'] or 0
    
    context = {
        'title': 'Wound Care Dashboard',
        'total_cases': total_cases,
        'active_cases': active_cases,
        'pending_cases': pending_cases,
        'resolved_cases': resolved_cases,
        'insured_cases': insured_cases,
        'uninsured_cases': uninsured_cases,
        'recent_wounds': recent_wounds,
        'pending_payments': pending_payments,
    }
    return render(request, 'wound_dashboard.html', context)