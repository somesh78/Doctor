from django.urls import path
from .views import *

urlpatterns = [
    path('register-doctor/', register_doctor, name='register-doctor'),
    path('login-doctor/', login_doctor, name='login-doctor'),
    path('add-patient/', add_patient, name='add-patient'),
    path('view-patients/', view_patients, name='view-patients'),
    path('update-patient/', update_patient, name='update-patient'),
    path('upload-images/', upload_images, name='upload-images'),
    path('upload-history/', upload_history, name='upload-history'),
    path('diagnose-image/<int:patient_id>/', diagnose_image, name='diagnose-image'),
]