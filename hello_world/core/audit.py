from auditlog.registry import auditlog
from . import models

# Register models for audit logging
auditlog.register(models.Patient)
auditlog.register(models.WoundCare)
auditlog.register(models.WoundTreatment)
auditlog.register(models.WoundBilling)
auditlog.register(models.Prescription)
auditlog.register(models.Appointment)
auditlog.register(models.LabRequest)
auditlog.register(models.OutPatientVisit)