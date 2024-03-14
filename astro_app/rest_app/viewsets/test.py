from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from core.models import ModelTest
from rest_app.serializers.test import TestSerializer


class TestViewSet(viewsets.ModelViewSet):
    queryset = ModelTest.objects.all()
    serializer_class = TestSerializer
    permission_classes = [AllowAny]
