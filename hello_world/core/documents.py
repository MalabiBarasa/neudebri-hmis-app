from django_elasticsearch_dsl import Document, Index
from django_elasticsearch_dsl.registries import registry
from elasticsearch_dsl import analyzer, tokenizer
from .models import Patient, WoundCare, Appointment, Prescription

# Define Elasticsearch index
@registry.register_document
class PatientDocument(Document):
    class Index:
        name = 'patients'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0
        }

    class Django:
        model = Patient
        fields = [
            'first_name',
            'last_name',
            'middle_name',
            'phone',
            'email',
            'address',
            'medical_record_number',
            'national_id',
        ]

        # Related fields
        related_models = [WoundCare, Appointment, Prescription]

    def get_queryset(self):
        return super().get_queryset().select_related()

    def get_instances_from_related(self, related_instance):
        """If related models are updated, update the patient's index"""
        if isinstance(related_instance, (WoundCare, Appointment, Prescription)):
            return related_instance.patient
        return super().get_instances_from_related(related_instance)

@registry.register_document
class WoundCareDocument(Document):
    class Index:
        name = 'wound_cases'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0
        }

    class Django:
        model = WoundCare
        fields = [
            'wound_id',
            'assessment_date',
            'appearance',
            'clinical_notes',
            'treatment_plan',
            'status',
        ]

        # Related fields
        related_models = [Patient]

    def get_queryset(self):
        return super().get_queryset().select_related('patient', 'wound_type', 'body_part')

    def prepare_patient_name(self, instance):
        return instance.patient.full_name

    def prepare_wound_type_name(self, instance):
        return instance.wound_type.name if instance.wound_type else ''

    def prepare_body_part_name(self, instance):
        return instance.body_part.name if instance.body_part else ''

@registry.register_document
class AppointmentDocument(Document):
    class Index:
        name = 'appointments'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0
        }

    class Django:
        model = Appointment
        fields = [
            'date',
            'status',
            'appointment_type',
            'notes',
        ]

        # Related fields
        related_models = [Patient]

    def get_queryset(self):
        return super().get_queryset().select_related('patient', 'doctor', 'clinic')

    def prepare_patient_name(self, instance):
        return instance.patient.full_name

    def prepare_doctor_name(self, instance):
        return instance.doctor.get_full_name()

    def prepare_clinic_name(self, instance):
        return instance.clinic.name

@registry.register_document
class PrescriptionDocument(Document):
    class Index:
        name = 'prescriptions'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0
        }

    class Django:
        model = Prescription
        fields = [
            'diagnosis',
            'instructions',
            'prescribed_at',
        ]

        # Related fields
        related_models = [Patient]

    def get_queryset(self):
        return super().get_queryset().select_related('patient', 'doctor')

    def prepare_patient_name(self, instance):
        return instance.patient.full_name

    def prepare_doctor_name(self, instance):
        return instance.doctor.get_full_name()