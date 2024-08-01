from django.db import models

class Patient(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

class MedicalImage(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    image_url = models.TextField()
    upload_date = models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField(default=True)

class Diagnosis(models.Model):
    image = models.ForeignKey(MedicalImage, on_delete=models.CASCADE)
    result = models.TextField()
    confidence = models.FloatField()
    diagnosed_at = models.DateField(auto_now_add=True)

class PatientHistory(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    description = models.TextField()
    document_url = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    