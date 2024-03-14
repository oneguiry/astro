from jinja2.nodes import Test
from rest_framework import serializers

from core.models import ModelTest


class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelTest
        fields = '__all__'
