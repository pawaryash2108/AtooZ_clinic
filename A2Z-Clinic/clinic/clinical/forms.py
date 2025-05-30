from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm, SetPasswordForm
from django.contrib.auth.models import User
from .models import Patient, Visit, MedicalDocument, Doctor

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))

class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['full_name', 'specialization', 'license_number', 'phone_number', 'profile_picture']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'specialization': forms.TextInput(attrs={'class': 'form-control'}),
            'license_number': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'}),
        }

class DoctorUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.is_staff = True
        if commit:
            user.save()
        return user

class PatientSearchForm(forms.Form):
    search = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Search by name, mobile or email'
    }))

class PatientForm(forms.ModelForm):
    date_of_birth = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    
    class Meta:
        model = Patient
        fields = [
            # Basic information
            'name', 'date_of_birth', 'age', 'gender', 'blood_group', 'marital_status',
            # Contact information
            'mobile', 'email', 'address',
            # Emergency contact
            'emergency_contact_name', 'emergency_contact_relationship', 'emergency_contact_number',
            # Medical history
            'past_medical_history', 'chronic_conditions', 'allergies', 'current_medications',
            'family_medical_history', 'vaccination_history',
            # Additional health information
            'height', 'weight', 'blood_pressure',
            # Lifestyle factors
            'occupation', 'smoking_status', 'alcohol_consumption', 'exercise_habits', 'dietary_restrictions',
            # Administrative information
            'insurance_provider', 'insurance_policy_number', 'preferred_pharmacy', 'preferred_language',
            # Advanced directives
            'has_advance_directive', 'advance_directive_details'
        ]
        widgets = {
            # Basic information
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'blood_group': forms.Select(attrs={'class': 'form-control'}),
            'marital_status': forms.Select(attrs={'class': 'form-control'}),
            
            # Contact information
            'mobile': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            
            # Emergency contact
            'emergency_contact_name': forms.TextInput(attrs={'class': 'form-control'}),
            'emergency_contact_relationship': forms.TextInput(attrs={'class': 'form-control'}),
            'emergency_contact_number': forms.TextInput(attrs={'class': 'form-control'}),
            
            # Medical history
            'past_medical_history': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'chronic_conditions': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'allergies': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'current_medications': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'family_medical_history': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'vaccination_history': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            
            # Additional health information
            'height': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'blood_pressure': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 120/80 mmHg'}),
            
            # Lifestyle factors
            'occupation': forms.TextInput(attrs={'class': 'form-control'}),
            'smoking_status': forms.TextInput(attrs={'class': 'form-control'}),
            'alcohol_consumption': forms.TextInput(attrs={'class': 'form-control'}),
            'exercise_habits': forms.TextInput(attrs={'class': 'form-control'}),
            'dietary_restrictions': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            
            # Administrative information
            'insurance_provider': forms.TextInput(attrs={'class': 'form-control'}),
            'insurance_policy_number': forms.TextInput(attrs={'class': 'form-control'}),
            'preferred_pharmacy': forms.TextInput(attrs={'class': 'form-control'}),
            'preferred_language': forms.TextInput(attrs={'class': 'form-control'}),
            
            # Advanced directives
            'has_advance_directive': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'advance_directive_details': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

class VisitForm(forms.ModelForm):
    follow_up_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    
    class Meta:
        model = Visit
        fields = [
            'visit_date', 'symptoms', 'diagnosis', 'prescribed_medicines', 
            'lab_tests_recommended', 'follow_up_date', 'blood_pressure', 
            'temperature', 'weight', 'height', 'notes'
        ]
        widgets = {
            'visit_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'symptoms': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'diagnosis': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'prescribed_medicines': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'lab_tests_recommended': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'blood_pressure': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 120/80 mmHg'}),
            'temperature': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'placeholder': 'e.g., 37.0 °C'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'in kg'}),
            'height': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'in cm'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class MedicalDocumentForm(forms.ModelForm):
    class Meta:
        model = MedicalDocument
        fields = ['title', 'document_type', 'file', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'document_type': forms.Select(attrs={'class': 'form-control'}),
            'file': forms.FileInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class UserProfileForm(forms.ModelForm):
    """Form for updating user credentials (username, email)"""
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class CustomPasswordChangeForm(PasswordChangeForm):
    """Custom form for changing password with Bootstrap styling"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs.update({'class': 'form-control'})
        self.fields['new_password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['new_password2'].widget.attrs.update({'class': 'form-control'}) 