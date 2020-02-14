from .models import WriteAPIOAuth2
from .views import write_to_collection
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def write_to_collection_oauth2(request, slug):
    return write_to_collection(request, slug, WriteAPIOAuth2)    
