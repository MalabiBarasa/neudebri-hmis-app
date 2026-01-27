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
