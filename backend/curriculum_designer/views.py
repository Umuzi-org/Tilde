from django.http import HttpResponse
from curriculum_tracking.models import ContentItem
from core.models import Curriculum

def index(request):
    Curriculum.objects.filter(manual_mode = True)
    return HttpResponse("Hello, world. You're at the polls index.")
