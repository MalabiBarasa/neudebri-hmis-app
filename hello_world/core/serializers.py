from rest_framework import serializers
from .models import *

class PatientSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(read_only=True)
    age = serializers.IntegerField(read_only=True)

    class Meta:
        model = Patient
        fields = [
            'id', 'medical_record_number', 'first_name', 'last_name',
            'middle_name', 'full_name', 'date_of_birth', 'age', 'gender',
            'phone', 'email', 'address', 'emergency_contact_name',
            'emergency_contact_phone', 'registration_date', 'is_active'
        ]

class WoundCareSerializer(serializers.ModelSerializer):
    patient = PatientSerializer(read_only=True)
    assessed_by_name = serializers.CharField(source='assessed_by.get_full_name', read_only=True)
    wound_type_name = serializers.CharField(source='wound_type.name', read_only=True)
    body_part_name = serializers.CharField(source='body_part.name', read_only=True)

    class Meta:
        model = WoundCare
        fields = [
            'id', 'wound_id', 'patient', 'assessment_date', 'assessed_by',
            'assessed_by_name', 'wound_type', 'wound_type_name', 'body_part',
            'body_part_name', 'laterality', 'length_cm', 'width_cm', 'depth_cm',
            'appearance', 'exudate', 'exudate_amount', 'pain_level', 'has_edema',
            'edema_grade', 'signs_of_infection', 'infection_notes', 'status',
            'next_visit_date', 'clinical_notes', 'treatment_plan', 'is_active'
        ]

class AppointmentSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.full_name', read_only=True)
    doctor_name = serializers.CharField(source='doctor.get_full_name', read_only=True)

    class Meta:
        model = Appointment
        fields = [
            'id', 'patient', 'patient_name', 'doctor', 'doctor_name',
            'clinic', 'date', 'status', 'appointment_type', 'notes'
        ]

class PrescriptionSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.full_name', read_only=True)
    doctor_name = serializers.CharField(source='doctor.get_full_name', read_only=True)

    class Meta:
        model = Prescription
        fields = [
            'id', 'patient', 'patient_name', 'doctor', 'doctor_name',
            'diagnosis', 'instructions', 'prescribed_date'
        ]