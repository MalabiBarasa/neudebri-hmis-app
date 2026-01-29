from django.urls import path
from . import views

urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),
    # Patient Register
    path("patients/", views.patient_list, name="patient_list"),
    path("patients/create/", views.patient_create, name="patient_create"),
    path("patients/<int:pk>/update/", views.patient_update, name="patient_update"),
    path("appointments/", views.appointment_list, name="appointment_list"),
    path("appointments/create/", views.appointment_create, name="appointment_create"),
    # Laboratory
    path("lab/requests/", views.lab_request_list, name="lab_request_list"),
    path("lab/requests/create/", views.lab_request_create, name="lab_request_create"),
    # Pharmacy
    path("prescriptions/", views.prescription_list, name="prescription_list"),
    path("prescriptions/create/", views.prescription_create, name="prescription_create"),
    # Out Patient
    path("outpatient/visits/", views.outpatient_visit_list, name="outpatient_visit_list"),
    path("outpatient/visits/create/", views.outpatient_visit_create, name="outpatient_visit_create"),
    # Nursing
    path("nursing/vitals/", views.vital_signs_list, name="vital_signs_list"),
    path("nursing/vitals/create/", views.vital_signs_create, name="vital_signs_create"),
    
    # Wound Care Management
    path("wounds/", views.wound_list, name="wound_list"),
    path("wounds/dashboard/", views.wound_dashboard, name="wound_dashboard"),
    path("wounds/create/", views.wound_create, name="wound_create"),
    path("wounds/<int:pk>/", views.wound_detail, name="wound_detail"),
    path("wounds/<int:pk>/update/", views.wound_update, name="wound_update"),
    path("wounds/<int:wound_id>/treatment/", views.wound_treatment_create, name="wound_treatment_create"),
    path("wounds/<int:wound_id>/followup/", views.wound_followup_create, name="wound_followup_create"),
    path("wounds/<int:wound_id>/billing/", views.wound_billing, name="wound_billing"),
]