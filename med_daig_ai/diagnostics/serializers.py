from rest_framework import serializers
from .models import *

class PatientSerializers(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'

class MedicalImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalImage
        fields = '__all__'

class DiagnosisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diagnosis
        fields = '__all__'

class PatientHistorySerializer:
    class Meta:
        model = PatientHistory
        fields = '__all__'
