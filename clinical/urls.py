from django.urls import path
from . import views

app_name = 'clinical'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Doctor
    path('doctor/setup/', views.doctor_setup, name='doctor_setup'),
    path('doctor/profile/', views.doctor_profile, name='doctor_profile'),
    path('doctor/change-password/', views.change_password, name='change_password'),
    
    # Patients
    path('patients/', views.patient_list, name='patient_list'),
    path('patients/add/', views.patient_add, name='patient_add'),
    path('patients/<int:pk>/', views.patient_detail, name='patient_detail'),
    path('patients/<int:pk>/edit/', views.patient_edit, name='patient_edit'),
    path('patients/<int:pk>/delete/', views.patient_delete, name='patient_delete'),
    
    # Visits
    path('visits/<int:pk>/', views.visit_detail, name='visit_detail'),
    path('visits/<int:pk>/delete/', views.visit_delete, name='visit_delete'),
    
    # Documents
    path('documents/', views.documents_list, name='documents_list'),
    path('documents/<int:pk>/delete/', views.document_delete, name='document_delete'),
] 