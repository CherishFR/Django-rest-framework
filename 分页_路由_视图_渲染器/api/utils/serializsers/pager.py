from rest_framework import serializers
from api import models
class PagerSerializer(serializers.ModelSerializer):
    class Meta:
        models = models.Role
        fields = "__all__"
