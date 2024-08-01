from supabase import create_client, Client
from django.conf import settings
from ..med_daig_ai import settings

supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)

def upload_to_supabase_storage(file, patient_id):
    file_path = f"medical-data/{patient_id}/{file.name}"
    response = supabase.storage().from_('medical-data').upload(file_path, file)
    if response.status_code == 200:
        return supabase.storage().from_('medical-data').get_public_url(file_path)
    else:
        return Exception('File upload failed')