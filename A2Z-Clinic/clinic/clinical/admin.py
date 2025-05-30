from django.contrib import admin
from .models import Patient, Visit, MedicalDocument, Doctor

class VisitInline(admin.TabularInline):
    model = Visit
    extra = 0

class MedicalDocumentInline(admin.TabularInline):
    model = MedicalDocument
    extra = 0

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'specialization', 'license_number', 'phone_number')
    search_fields = ('full_name', 'license_number')

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'gender', 'blood_group', 'mobile', 'email', 'created_at')
    list_filter = ('gender', 'blood_group', 'created_at')
    search_fields = ('name', 'mobile', 'email')
    inlines = [VisitInline, MedicalDocumentInline]

@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    list_display = ('patient', 'visit_date', 'diagnosis')
    list_filter = ('visit_date',)
    search_fields = ('patient__name', 'diagnosis')

@admin.register(MedicalDocument)
class MedicalDocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'document_type', 'patient', 'visit', 'uploaded_at')
    list_filter = ('document_type', 'uploaded_at')
    search_fields = ('title', 'patient__name')
