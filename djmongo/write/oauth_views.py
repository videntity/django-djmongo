from .models import WriteAPIOAuth2
from .views import write_to_collection

@csrf_exempt
def write_to_collection_oauth2(request, slug):
    return write_to_collection(request, slug, WriteAPIOAuth2)    
