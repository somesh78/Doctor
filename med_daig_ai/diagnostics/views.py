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
def register_patient(req):
    email = req.data.get('email')
    password = req.data.get('password')
    name = req.data.get('name')

    try:
        response = supabase.auth.sign_up({
            'email': email,
            'password': password,
        })

        if response.user:
            patient = Patient.objects.create(name=name, email=email)    
            serializer = PatientSerializers(patient)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'Registration failed in Supabase'}, status=status.HTTP_400_BAD_REQUEST)
    except AuthApiError as e:
        logger.error(f"Error during patient registration: {str(e)}")
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': 'An unexpected error occurred', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['POST'])
def login_patient   (req):
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
def upload_images(req):
    patient_email = req.data.get('email')
    patient = Patient.objects.filter(email=patient_email).first()
    if not patient:
        return Response({'error': 'Patient not found'}, status=status.HTTP_404_NOT_FOUND)

    images = req.FILES.getlist('images')
    for image in images:
        image_url = upload_to_supabase_storage(image, patient.id)
        MedicalImage.objects.create(patient=patient, image_url=image_url, processed=False)

    return Response({'message': 'Images uploaded successfully'}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def upload_history(req):
    patient_email = req.data.get('email')
    patient = Patient.objects.filter(email=patient_email).first()
    if not patient:
        return Response({'error': 'Patient not found'}, status=status.HTTP_404_NOT_FOUND)

    document = req.FILES.get('document')
    description = req.data.get('description')
    document_url = upload_to_supabase_storage(document, patient.id)
    PatientHistory.objects.create(patient=patient, description=description,document_url=document_url)

    return Response({'message': 'History uploaded successfully'}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def diagnose_image(req, patient_id):
    # patient = get_object_or_404(Patient, id=patient_id)
    # images = MedicalImage.objects.filter(patient=patient, processed=False)
    # history = PatientHistory.objects.filter(patient=patient)
    
    # # Process all images and history
    # results = []
    # for image in images:
    #     img = Image.open(image.image_url)
    #     processed_image = preprocess_image(img)
    #     prediction = model.predict(processed_image)
    #     result = np.argmax(prediction, axis=1)
    #     confidence = np.max(prediction, axis=1)
        
    #     # Save diagnosis result
    #     diagnosis = Diagnosis.objects.create(
    #         image=image,
    #         result=str(result[0]),
    #         confidence=confidence[0],
    #         diagnosed_at=timezone.now()
    #     )
        
    #     results.append({
    #         'image_id': image.id,
    #         'result': diagnosis.result,
    #         'confidence': diagnosis.confidence,
    #         'diagnosed_at': diagnosis.diagnosed_at
    #     })
        
    #     # Mark the image as processed
    #     image.processed = True
    #     image.save()
    
    # return JsonResponse({'results': results, 'history': list(history.values())})
    pass
