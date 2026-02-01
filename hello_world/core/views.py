from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django_tables2 import RequestConfig
from django.db.models import Q
from datetime import datetime
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


# Phase 2 Enhancement Views

@login_required
def backup_database(request):
    """Create database backup"""
    if not request.user.is_staff:
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('dashboard')
    
    try:
        from django.core.management import call_command
        call_command('dbbackup')
        messages.success(request, 'Database backup created successfully.')
    except Exception as e:
        messages.error(request, f'Backup failed: {str(e)}')
    
    return redirect('admin_dashboard')

@login_required
def audit_trail(request, model_name, pk):
    """View audit trail for a specific model instance"""
    from auditlog.models import LogEntry
    from django.contrib.contenttypes.models import ContentType
    
    try:
        content_type = ContentType.objects.get(model=model_name.lower())
        history = LogEntry.objects.filter(
            content_type=content_type,
            object_id=pk
        ).order_by('-timestamp')
        
        context = {
            'title': f'Audit Trail - {model_name} #{pk}',
            'history': history,
            'model_name': model_name,
            'object_id': pk,
        }
        return render(request, 'audit_trail.html', context)
    except ContentType.DoesNotExist:
        messages.error(request, f'Model {model_name} not found.')
        return redirect('dashboard')

@login_required
def advanced_analytics(request):
    """Advanced analytics dashboard with interactive charts"""
    import plotly.graph_objects as go
    from plotly.offline import plot
    from django.db.models import Count, Q
    from datetime import timedelta

    # Wound healing timeline (last 90 days)
    ninety_days_ago = timezone.now() - timedelta(days=90)
    wounds = WoundCare.objects.filter(assessment_date__gte=ninety_days_ago)

    # Healing progress chart
    healing_data = wounds.filter(status='resolved').values('assessment_date').annotate(
        count=Count('id')
    ).order_by('assessment_date')

    active_data = wounds.filter(status='active').values('assessment_date').annotate(
        count=Count('id')
    ).order_by('assessment_date')

    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(
        x=[d['assessment_date'] for d in healing_data],
        y=[d['count'] for d in healing_data],
        mode='lines+markers',
        name='Resolved Cases',
        line=dict(color='green')
    ))
    fig1.add_trace(go.Scatter(
        x=[d['assessment_date'] for d in active_data],
        y=[d['count'] for d in active_data],
        mode='lines+markers',
        name='Active Cases',
        line=dict(color='orange')
    ))
    fig1.update_layout(
        title='Wound Care Progress Over Time',
        xaxis_title='Date',
        yaxis_title='Number of Cases'
    )

    # Wound type distribution
    wound_type_data = WoundCare.objects.values('wound_type__name').annotate(
        count=Count('id')
    ).order_by('-count')[:10]

    fig2 = go.Figure(data=[
        go.Bar(
            x=[item['wound_type__name'] or 'Unknown' for item in wound_type_data],
            y=[item['count'] for item in wound_type_data],
            marker_color='lightblue'
        )
    ])
    fig2.update_layout(
        title='Wound Types Distribution',
        xaxis_title='Wound Type',
        yaxis_title='Number of Cases'
    )

    # Insurance coverage pie chart
    insurance_data = WoundCare.objects.aggregate(
        insured=Count('id', filter=Q(insurance_covers=True)),
        uninsured=Count('id', filter=Q(insurance_covers=False))
    )

    fig3 = go.Figure(data=[
        go.Pie(
            labels=['Insured', 'Uninsured'],
            values=[insurance_data['insured'], insurance_data['uninsured']],
            marker_colors=['lightgreen', 'lightcoral']
        )
    ])
    fig3.update_layout(title='Insurance Coverage Distribution')

    context = {
        'title': 'Advanced Analytics Dashboard',
        'chart1': fig1.to_html(full_html=False),
        'chart2': fig2.to_html(full_html=False),
        'chart3': fig3.to_html(full_html=False),
    }
    return render(request, 'advanced_analytics.html', context)


# Search and Filtering Views

@login_required
def global_search(request):
    """
    Global search across all indexed content
    """
    query = request.GET.get('q', '').strip()
    search_type = request.GET.get('type', 'all')
    results = {
        'patients': [],
        'wound_cases': [],
        'appointments': [],
        'prescriptions': [],
    }

    if query and len(query) >= 2:
        try:
            # Try Elasticsearch first
            if search_type in ['all', 'patients']:
                from .documents import PatientDocument
                patient_search = PatientDocument.search().query(
                    'multi_match',
                    query=query,
                    fields=['first_name', 'last_name', 'medical_record_number', 'phone', 'email']
                )
                results['patients'] = patient_search[:10].execute()

            if search_type in ['all', 'wound_cases']:
                from .documents import WoundCareDocument
                wound_search = WoundCareDocument.search().query(
                    'multi_match',
                    query=query,
                    fields=['wound_id', 'appearance', 'clinical_notes', 'patient_name', 'wound_type_name']
                )
                results['wound_cases'] = wound_search[:10].execute()

            if search_type in ['all', 'appointments']:
                from .documents import AppointmentDocument
                appointment_search = AppointmentDocument.search().query(
                    'multi_match',
                    query=query,
                    fields=['patient_name', 'doctor_name', 'notes']
                )
                results['appointments'] = appointment_search[:10].execute()

            if search_type in ['all', 'prescriptions']:
                from .documents import PrescriptionDocument
                prescription_search = PrescriptionDocument.search().query(
                    'multi_match',
                    query=query,
                    fields=['diagnosis', 'instructions', 'patient_name', 'doctor_name']
                )
                results['prescriptions'] = prescription_search[:10].execute()

        except Exception as e:
            # Fallback to database search if Elasticsearch is not available
            messages.info(request, 'Using database search (Elasticsearch not available)')

            if search_type in ['all', 'patients']:
                results['patients'] = Patient.objects.filter(
                    Q(first_name__icontains=query) |
                    Q(last_name__icontains=query) |
                    Q(medical_record_number__icontains=query) |
                    Q(phone__icontains=query) |
                    Q(email__icontains=query)
                )[:10]

            if search_type in ['all', 'wound_cases']:
                results['wound_cases'] = WoundCare.objects.filter(
                    Q(wound_id__icontains=query) |
                    Q(appearance__icontains=query) |
                    Q(clinical_notes__icontains=query)
                ).select_related('patient', 'wound_type')[:10]

            if search_type in ['all', 'appointments']:
                results['appointments'] = Appointment.objects.filter(
                    Q(notes__icontains=query)
                ).select_related('patient', 'doctor')[:10]

            if search_type in ['all', 'prescriptions']:
                results['prescriptions'] = Prescription.objects.filter(
                    Q(diagnosis__icontains=query) |
                    Q(instructions__icontains=query)
                ).select_related('patient', 'doctor')[:10]

    context = {
        'title': 'Global Search',
        'query': query,
        'search_type': search_type,
        'results': results,
        'total_results': sum(len(result) for result in results.values()),
    }
    return render(request, 'global_search.html', context)

@login_required
def advanced_search(request):
    """
    Advanced search with filters and facets
    """
    query = request.GET.get('q', '')
    search_type = request.GET.get('type', 'all')
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')
    doctor = request.GET.get('doctor', '')
    clinic = request.GET.get('clinic', '')

    results = {
        'patients': [],
        'wound_cases': [],
        'appointments': [],
        'prescriptions': [],
    }

    if query or date_from or date_to or doctor or clinic:
        # Build complex Q objects for filtering
        patient_filters = Q()
        wound_filters = Q()
        appointment_filters = Q()
        prescription_filters = Q()

        if query:
            patient_filters &= (Q(first_name__icontains=query) |
                              Q(last_name__icontains=query) |
                              Q(phone__icontains=query) |
                              Q(id_number__icontains=query))
            wound_filters &= (Q(wound_id__icontains=query) |
                            Q(appearance__icontains=query) |
                            Q(clinical_notes__icontains=query))
            appointment_filters &= Q(notes__icontains=query)
            prescription_filters &= (Q(diagnosis__icontains=query) |
                                    Q(instructions__icontains=query))

        if date_from:
            try:
                date_from_obj = datetime.strptime(date_from, '%Y-%m-%d')
                wound_filters &= Q(created_at__date__gte=date_from_obj)
                appointment_filters &= Q(appointment_date__date__gte=date_from_obj)
                prescription_filters &= Q(prescribed_at__date__gte=date_from_obj)
            except ValueError:
                pass

        if date_to:
            try:
                date_to_obj = datetime.strptime(date_to, '%Y-%m-%d')
                wound_filters &= Q(created_at__date__lte=date_to_obj)
                appointment_filters &= Q(appointment_date__date__lte=date_to_obj)
                prescription_filters &= Q(prescribed_at__date__lte=date_to_obj)
            except ValueError:
                pass

        if doctor:
            try:
                doctor_id = int(doctor)
                wound_filters &= Q(doctor_id=doctor_id)
                appointment_filters &= Q(doctor_id=doctor_id)
                prescription_filters &= Q(doctor_id=doctor_id)
            except ValueError:
                pass

        if clinic:
            try:
                clinic_id = int(clinic)
                appointment_filters &= Q(clinic_id=clinic_id)
            except ValueError:
                pass

        # Apply filters
        if search_type in ['all', 'patients']:
            results['patients'] = Patient.objects.filter(patient_filters)[:20]

        if search_type in ['all', 'wound_cases']:
            results['wound_cases'] = WoundCare.objects.filter(wound_filters).select_related('patient', 'wound_type')[:20]

        if search_type in ['all', 'appointments']:
            results['appointments'] = Appointment.objects.filter(appointment_filters).select_related('patient', 'doctor', 'clinic')[:20]

        if search_type in ['all', 'prescriptions']:
            results['prescriptions'] = Prescription.objects.filter(prescription_filters).select_related('patient', 'doctor')[:20]

    # Get filter options
    doctors = User.objects.filter(is_staff=True).order_by('first_name', 'last_name')
    clinics = Clinic.objects.all().order_by('name')

    context = {
        'title': 'Advanced Search',
        'query': query,
        'search_type': search_type,
        'date_from': date_from,
        'date_to': date_to,
        'doctor': doctor,
        'clinic': clinic,
        'results': results,
        'total_results': sum(len(result) for result in results.values()),
        'doctors': doctors,
        'clinics': clinics,
    }
    return render(request, 'advanced_search.html', context)