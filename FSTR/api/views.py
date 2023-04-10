from .serializers import PerevalAddedSerializer
from rest_framework import viewsets
from .models import PerevalAdded


class PerevalAddedViewSet(viewsets.ModelViewSet):
    serializer_class = PerevalAddedSerializer
    queryset = PerevalAdded.objects.all()
