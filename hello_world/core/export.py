import csv
from openpyxl import Workbook
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Patient, WoundCare

@login_required
def export_patients_csv(request):
    """Export patients to CSV"""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="patients.csv"'

    writer = csv.writer(response)
    writer.writerow([
        'MRN', 'Full Name', 'Date of Birth', 'Age', 'Gender',
        'Phone', 'Email', 'Address', 'Registration Date'
    ])

    for patient in Patient.objects.filter(is_active=True):
        writer.writerow([
            patient.medical_record_number,
            patient.full_name,
            patient.date_of_birth,
            patient.age,
            patient.get_gender_display(),
            patient.phone,
            patient.email or '',
            patient.address or '',
            patient.registration_date.date(),
        ])

    return response

@login_required
def export_wounds_excel(request):
    """Export wound cases to Excel"""
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="wound_cases.xlsx"'

    wb = Workbook()
    ws = wb.active
    ws.title = "Wound Cases"

    # Header row
    headers = [
        'Case ID', 'Patient MRN', 'Patient Name', 'Wound Type', 'Body Part',
        'Assessment Date', 'Status', 'Pain Level', 'Insurance Covered'
    ]
    ws.append(headers)

    # Data rows
    for wound in WoundCare.objects.select_related('patient', 'wound_type', 'body_part'):
        ws.append([
            wound.wound_id,
            wound.patient.medical_record_number,
            wound.patient.full_name,
            wound.wound_type.name if wound.wound_type else '',
            wound.body_part.name if wound.body_part else '',
            wound.assessment_date.date(),
            wound.get_status_display(),
            wound.pain_level,
            'Yes' if wound.insurance_covers else 'No',
        ])

    wb.save(response)
    return response

@login_required
def export_wounds_pdf(request):
    """Export wound cases to PDF"""
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="wound_cases.pdf"'

    doc = SimpleDocTemplate(response, pagesize=letter)
    elements = []

    # Data
    data = [['Case ID', 'Patient', 'Type', 'Status', 'Date', 'Insurance']]

    for wound in WoundCare.objects.select_related('patient', 'wound_type'):
        data.append([
            wound.wound_id,
            wound.patient.full_name,
            wound.wound_type.name if wound.wound_type else 'N/A',
            wound.get_status_display(),
            str(wound.assessment_date.date()),
            'Yes' if wound.insurance_covers else 'No',
        ])

    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    elements.append(table)
    doc.build(elements)
    return response