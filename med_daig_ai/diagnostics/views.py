from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from .supabase import *

@api_view(['POST'])
def register_user(req):
    serializer = PatientHistorySerializer(data=req.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login_user(req):
    pass

@api_view(['POST'])
def upload_history(req):
    pass

@api_view(['POST'])
def upload_image(req):
    pass

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
