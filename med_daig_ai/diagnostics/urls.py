from django.urls import path
from .views import *

urlpatterns = [
    path('register/', register_patient, name='register_patient'),
    path('login/', login_patient, name='login_patient'),
    path('upload_images/', upload_images, name='upload_image'),
    path('upload_history/', upload_history, name='upload_history'),
]