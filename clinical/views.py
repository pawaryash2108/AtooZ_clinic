from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.db.models import Q, Count
from django.contrib import messages
from django.http import HttpResponseForbidden
from .models import Patient, Visit, MedicalDocument, Doctor
from .forms import (
    CustomAuthenticationForm, PatientForm, VisitForm, MedicalDocumentForm, 
    PatientSearchForm, DoctorForm, DoctorUserCreationForm, UserProfileForm,
    CustomPasswordChangeForm
)

def doctor_exists():
    return Doctor.objects.exists()

def is_superuser(user):
    return user.is_superuser

def login_view(request):
    # Redirect to dashboard if already logged in
    if request.user.is_authenticated:
        return redirect('clinical:dashboard')
        
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                # Check if the user is a doctor or superuser
                is_doctor = hasattr(user, 'doctor_profile') or user.is_superuser
                if is_doctor:
                    login(request, user)
                    # Get the next parameter or default to dashboard
                    next_url = request.GET.get('next', 'clinical:dashboard')
                    return redirect(next_url)
                else:
                    messages.error(request, "Access denied. Only doctors can log in.")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'clinical/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('clinical:login')

@user_passes_test(is_superuser)
def doctor_setup(request):
    # Check if a doctor already exists
    if doctor_exists() and not request.user.is_superuser:
        messages.error(request, "A doctor account already exists.")
        return redirect('clinical:dashboard')
    
    if request.method == 'POST':
        user_form = DoctorUserCreationForm(request.POST)
        doctor_form = DoctorForm(request.POST, request.FILES)
        
        if user_form.is_valid() and doctor_form.is_valid():
            user = user_form.save()
            doctor = doctor_form.save(commit=False)
            doctor.user = user
            doctor.save()
            
            messages.success(request, f"Doctor account for {doctor.full_name} created successfully.")
            return redirect('clinical:dashboard')
    else:
        user_form = DoctorUserCreationForm()
        doctor_form = DoctorForm()
    
    context = {
        'user_form': user_form,
        'doctor_form': doctor_form,
    }
    return render(request, 'clinical/doctor_setup.html', context)

@login_required
def doctor_profile(request):
    try:
        doctor = request.user.doctor_profile
    except Doctor.DoesNotExist:
        if request.user.is_superuser:
            return redirect('clinical:doctor_setup')
        return HttpResponseForbidden("Access denied")
    
    if request.method == 'POST':
        form = DoctorForm(request.POST, request.FILES, instance=doctor)
        user_form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid() and user_form.is_valid():
            form.save()
            user_form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('clinical:doctor_profile')
    else:
        form = DoctorForm(instance=doctor)
        user_form = UserProfileForm(instance=request.user)
    
    context = {
        'form': form,
        'user_form': user_form,
        'doctor': doctor,
    }
    return render(request, 'clinical/doctor_profile.html', context)

@login_required
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            # Keep the user logged in
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('clinical:doctor_profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = CustomPasswordChangeForm(request.user)
    
    return render(request, 'clinical/change_password.html', {
        'form': form
    })

@login_required
def dashboard(request):
    # Get counts for dashboard
    total_patients = Patient.objects.count()
    total_visits = Visit.objects.count()
    recent_visits = Visit.objects.select_related('patient').order_by('-visit_date')[:5]
    
    # Get statistics
    gender_stats = Patient.objects.values('gender').annotate(count=Count('gender'))
    visits_by_month = Visit.objects.extra(select={'month': "strftime('%%m', visit_date)"}).values('month').annotate(count=Count('id')).order_by('month')
    
    context = {
        'total_patients': total_patients,
        'total_visits': total_visits,
        'recent_visits': recent_visits,
        'gender_stats': gender_stats,
        'visits_by_month': visits_by_month,
    }
    return render(request, 'clinical/dashboard.html', context)

@login_required
def patient_list(request):
    form = PatientSearchForm(request.GET)
    patients = Patient.objects.all().order_by('-created_at')
    
    if form.is_valid():
        search_query = form.cleaned_data.get('search')
        if search_query:
            patients = patients.filter(
                Q(name__icontains=search_query) | 
                Q(mobile__icontains=search_query) | 
                Q(email__icontains=search_query)
            )
    
    context = {
        'patients': patients,
        'form': form,
    }
    return render(request, 'clinical/patient_list.html', context)

@login_required
def patient_add(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            patient = form.save()
            messages.success(request, f"Patient {patient.name} added successfully.")
            return redirect('clinical:patient_detail', pk=patient.pk)
    else:
        form = PatientForm()
    
    context = {
        'form': form,
        'title': 'Add New Patient',
    }
    return render(request, 'clinical/patient_form.html', context)

@login_required
def patient_detail(request, pk):
    try:
        patient = get_object_or_404(Patient, pk=pk)
        visits = Visit.objects.filter(patient=patient).order_by('-visit_date')
        documents = MedicalDocument.objects.filter(patient=patient).order_by('-uploaded_at')
        
        # Form for adding a new visit
        if request.method == 'POST':
            if 'visit_form' in request.POST:
                visit_form = VisitForm(request.POST)
                if visit_form.is_valid():
                    visit = visit_form.save(commit=False)
                    visit.patient = patient
                    visit.save()
                    messages.success(request, "Visit record added successfully.")
                    return redirect('clinical:patient_detail', pk=patient.pk)
            elif 'document_form' in request.POST:
                document_form = MedicalDocumentForm(request.POST, request.FILES)
                if document_form.is_valid():
                    document = document_form.save(commit=False)
                    document.patient = patient
                    document.save()
                    messages.success(request, "Document uploaded successfully.")
                    return redirect('clinical:patient_detail', pk=patient.pk)
        else:
            visit_form = VisitForm()
            document_form = MedicalDocumentForm()
        
        context = {
            'patient': patient,
            'visits': visits,
            'documents': documents,
            'visit_form': visit_form,
            'document_form': document_form,
        }
        return render(request, 'clinical/patient_detail.html', context)
    except Exception as e:
        messages.error(request, f"Error accessing patient details: {str(e)}")
        return redirect('clinical:patient_list')

@login_required
def patient_edit(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    
    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            messages.success(request, f"Patient {patient.name} updated successfully.")
            return redirect('clinical:patient_detail', pk=patient.pk)
    else:
        form = PatientForm(instance=patient)
    
    context = {
        'form': form,
        'patient': patient,
        'title': 'Edit Patient',
    }
    return render(request, 'clinical/patient_form.html', context)

@login_required
def visit_detail(request, pk):
    visit = get_object_or_404(Visit, pk=pk)
    
    if request.method == 'POST':
        form = VisitForm(request.POST, instance=visit)
        if form.is_valid():
            form.save()
            messages.success(request, "Visit updated successfully.")
            return redirect('clinical:patient_detail', pk=visit.patient.pk)
    else:
        form = VisitForm(instance=visit)
    
    context = {
        'form': form,
        'visit': visit,
    }
    return render(request, 'clinical/visit_detail.html', context)

@login_required
def documents_list(request):
    documents = MedicalDocument.objects.all().order_by('-uploaded_at')
    
    context = {
        'documents': documents,
    }
    return render(request, 'clinical/documents_list.html', context)

@login_required
def patient_delete(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    
    if request.method == 'POST':
        patient_name = patient.name
        patient.delete()
        messages.success(request, f"Patient {patient_name} deleted successfully.")
        return redirect('clinical:patient_list')
    
    context = {
        'patient': patient,
    }
    return render(request, 'clinical/patient_delete_confirm.html', context)

@login_required
def visit_delete(request, pk):
    visit = get_object_or_404(Visit, pk=pk)
    patient_id = visit.patient.id
    
    if request.method == 'POST':
        visit.delete()
        messages.success(request, "Visit record deleted successfully.")
        return redirect('clinical:patient_detail', pk=patient_id)
    
    context = {
        'visit': visit,
    }
    return render(request, 'clinical/visit_delete_confirm.html', context)

@login_required
def document_delete(request, pk):
    document = get_object_or_404(MedicalDocument, pk=pk)
    patient_id = document.patient.id
    
    if request.method == 'POST':
        document.delete()
        messages.success(request, "Document deleted successfully.")
        return redirect('clinical:patient_detail', pk=patient_id)
    
    context = {
        'document': document,
    }
    return render(request, 'clinical/document_delete_confirm.html', context)
