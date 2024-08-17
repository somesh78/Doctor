from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from .supabase import *
from .ai_model import *
from django.views.decorators.csrf import csrf_exempt
from gotrue.errors import AuthApiError
import logging

logger = logging.getLogger(__name__)

@api_view(['POST'])
def register_doctor(req):
    email = req.data.get('email')
    password = req.data.get('password')
    name = req.data.get('name')

    try:
        response = supabase.auth.sign_up({
            'email': email,
            'password': password,
        })

        if response.user:
            doctor = Doctor.objects.create(name=name, email=email)    
            serializer = PatientSerializers(doctor)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'Registration failed in Supabase'}, status=status.HTTP_400_BAD_REQUEST)
    except AuthApiError as e:
        logger.error(f"Error during doctor registration: {str(e)}")
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': 'An unexpected error occurred', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['POST'])
def login_doctor(req):
    email = req.data.get('email')
    password = req.data.get('password')
    
    try:
        response = supabase.auth.sign_in_with_password({
            'email': email,
            'password': password,
        })
        if response.user:
            return Response({'message': 'Login Successful', 'session': response.session}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid login credentials'}, status=status.HTTP_400_BAD_REQUEST)
    except AuthApiError as e:
        return Response({'error': f'Login Failed: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': 'An unexpected error occurred', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def add_patient(req):
    doctor_email = req.data.get('doctor_email')
    doctor = Doctor.objects.filter(email=doctor_email).first()

    if not doctor:
        return Response({'error': 'Doctor not found'}, status=status.HTTP_404_NOT_FOUND)
    
    name = req.data.get('name')
    age = req.data.get('age')
    if not name:
        return Response({'error': 'Name is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        respnose = supabase.table('patient').insert({
            'name': name,
            'age': age,
            'doctor_id': doctor.id
        }).execute()

        if respnose.data:
            patient_id = respnose.data[0]['id']
            patient = Patient.objects.create(id=patient_id, doctor=doctor, name=name, age=age)
            serializer = PatientSerializers(patient)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'Patient not created in Supabase'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': 'An unexpected error occurred', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def view_patients(req):
    doctor_email = req.data.get('doctor_email')
    doctor = Doctor.objects.filter(email=doctor_email).first()

    if not doctor:
        return Response({'error': 'Doctor not found'}, status=status.HTTP_404_NOT_FOUND)

    try:
        patients = Patient.objects.filter(doctor=doctor)
        serializer = PatientSerializers(patients, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': 'An unexpected error occurred', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['PUT'])
def update_patient(req):
    patient_id = req.data.get('patient_id')
    patient = Patient.objects.filter(id=patient_id).first()
    if not patient:
        return Response({'error': 'Patient not found'}, status=status.HTTP_404_NOT_FOUND)
    
    name = req.data.get('name')
    age = req.data.get('age')

    try:
        supabase_update = supabase.table('patient').update({
            'name': name,
            'age' : age
        }).eq('id', patient_id).execute()

        if supabase_update.data:
            if name:
                patient.name = name
            if age is not None:
                patient.age = age
            patient.save()
            serializer = PatientSerializers(patient)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Patient not updated in Supabase'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': 'An unexpected error occurred', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def upload_images(req):
    patient_id = req.data.get('patient_id')
    patient = Patient.objects.filter(id=patient_id).first()
    if not patient:
        return Response({'error': 'Patient not found'}, status=status.HTTP_404_NOT_FOUND)

    images = req.FILES.getlist('images')
    for image in images:
        image_url = upload_to_supabase_storage(image, patient.id)
        MedicalImage.objects.create(patient=patient, image_url=image_url, processed=False)

    return Response({'message': 'Images uploaded successfully'}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def upload_history(req):
    patient_id = req.data.get('patient_id')
    patient = Patient.objects.filter(id=patient_id).first()
    if not patient:
        return Response({'error': 'Patient not found'}, status=status.HTTP_404_NOT_FOUND)

    lab_report = req.FILES.get('document')
    lab_report_url = upload_to_supabase_storage(lab_report, patient.id)
    PatientHistory.objects.create(patient=patient, lab_report=lab_report,lab_report_url=lab_report_url)

    return Response({'message': 'History uploaded successfully'}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def diagnose_image(req, patient_id):
    pass
