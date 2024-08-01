from django.urls import path
from .views import *

urlpatterns = [
    path('register', register_user, name='register_user'),
    path('login', login_user, name='login_user'),
    path('upload', upload_image, name='upload_image'),
    path('dianosis/<int:image_id>', view_diagnosis, name='view_diagnosis')
]