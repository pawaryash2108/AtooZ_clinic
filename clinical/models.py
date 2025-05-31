from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor_profile')
    full_name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    license_number = models.CharField(max_length=50, unique=True)
    phone_number = models.CharField(max_length=15)
    profile_picture = models.ImageField(upload_to='doctor_profiles/', null=True, blank=True)
    
    def __str__(self):
        return self.full_name

class Patient(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    
    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ]
    
    MARITAL_STATUS_CHOICES = [
        ('S', 'Single'),
        ('M', 'Married'),
        ('D', 'Divorced'),
        ('W', 'Widowed'),
        ('O', 'Other'),
    ]
    
    # Basic information
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES, null=True, blank=True)
    marital_status = models.CharField(max_length=1, choices=MARITAL_STATUS_CHOICES, null=True, blank=True)
    
    # Contact information
    mobile = models.CharField(max_length=15)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    
    # Emergency contact
    emergency_contact_name = models.CharField(max_length=100, null=True, blank=True)
    emergency_contact_relationship = models.CharField(max_length=50, null=True, blank=True)
    emergency_contact_number = models.CharField(max_length=15, null=True, blank=True)
    
    # Medical history
    past_medical_history = models.TextField(blank=True, null=True, help_text="Previous significant illnesses, surgeries, hospitalizations")
    chronic_conditions = models.TextField(blank=True, null=True, help_text="Ongoing health conditions requiring management")
    allergies = models.TextField(blank=True, null=True, help_text="Medications, food, environmental allergies and reactions")
    current_medications = models.TextField(blank=True, null=True, help_text="Include dosage, frequency, and duration")
    family_medical_history = models.TextField(blank=True, null=True, help_text="Medical conditions present in immediate family members")
    vaccination_history = models.TextField(blank=True, null=True, help_text="Major vaccinations received and dates")
    
    # Additional health information
    height = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="Height in cm")
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="Weight in kg")
    blood_pressure = models.CharField(max_length=20, null=True, blank=True, help_text="Last recorded blood pressure")
    
    # Lifestyle factors
    occupation = models.CharField(max_length=100, null=True, blank=True)
    smoking_status = models.CharField(max_length=50, null=True, blank=True, help_text="Never, Former, Current (packs/day)")
    alcohol_consumption = models.CharField(max_length=100, null=True, blank=True, help_text="None, Occasional, Moderate, Heavy")
    exercise_habits = models.CharField(max_length=100, null=True, blank=True, help_text="Frequency and type")
    dietary_restrictions = models.TextField(null=True, blank=True)
    
    # Administrative information
    insurance_provider = models.CharField(max_length=100, null=True, blank=True)
    insurance_policy_number = models.CharField(max_length=50, null=True, blank=True)
    preferred_pharmacy = models.CharField(max_length=100, null=True, blank=True)
    preferred_language = models.CharField(max_length=50, null=True, blank=True, default="English")
    
    # Advanced directives
    has_advance_directive = models.BooleanField(default=False)
    advance_directive_details = models.TextField(null=True, blank=True, help_text="Details on living will, healthcare proxy, etc.")
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

class Visit(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='visits')
    visit_date = models.DateTimeField(default=timezone.now)
    symptoms = models.TextField()
    diagnosis = models.TextField()
    prescribed_medicines = models.TextField()
    lab_tests_recommended = models.TextField(blank=True, null=True)
    follow_up_date = models.DateField(null=True, blank=True)
    blood_pressure = models.CharField(max_length=20, blank=True, null=True)
    temperature = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    height = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.patient.name} - {self.visit_date.strftime('%Y-%m-%d')}"
    
    class Meta:
        ordering = ['-visit_date']

class MedicalDocument(models.Model):
    DOCUMENT_TYPES = [
        ('LAB', 'Laboratory Result'),
        ('SCAN', 'Scan/X-ray'),
        ('PRESCRIPTION', 'Prescription'),
        ('REPORT', 'Medical Report'),
        ('OTHER', 'Other')
    ]
    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='documents')
    visit = models.ForeignKey(Visit, on_delete=models.CASCADE, related_name='documents', null=True, blank=True)
    title = models.CharField(max_length=100)
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES, default='OTHER')
    file = models.FileField(upload_to='medical_documents/')
    description = models.TextField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
