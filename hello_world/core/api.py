from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count, Q
from datetime import timedelta
from django.utils import timezone
from .models import *
from .serializers import *

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get patient statistics"""
        total_patients = self.queryset.count()
        active_patients = self.queryset.filter(is_active=True).count()
        male_patients = self.queryset.filter(gender='M').count()
        female_patients = self.queryset.filter(gender='F').count()

        return Response({
            'total_patients': total_patients,
            'active_patients': active_patients,
            'male_patients': male_patients,
            'female_patients': female_patients,
        })

class WoundCareViewSet(viewsets.ModelViewSet):
    queryset = WoundCare.objects.select_related(
        'patient', 'wound_type', 'body_part', 'assessed_by'
    )
    serializer_class = WoundCareSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get wound care statistics"""
        total_cases = self.queryset.count()
        active_cases = self.queryset.filter(status='active').count()
        resolved_cases = self.queryset.filter(status='resolved').count()
        pending_cases = self.queryset.filter(status='pending').count()

        # Recent cases (last 30 days)
        thirty_days_ago = timezone.now() - timedelta(days=30)
        recent_cases = self.queryset.filter(assessment_date__gte=thirty_days_ago).count()

        return Response({
            'total_cases': total_cases,
            'active_cases': active_cases,
            'resolved_cases': resolved_cases,
            'pending_cases': pending_cases,
            'recent_cases': recent_cases,
        })

class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.select_related('patient', 'doctor', 'clinic')
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]

class PrescriptionViewSet(viewsets.ModelViewSet):
    queryset = Prescription.objects.select_related('patient', 'doctor')
    serializer_class = PrescriptionSerializer
    permission_classes = [permissions.IsAuthenticated]