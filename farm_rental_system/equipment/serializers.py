from django.contrib.auth.models import Group
from rest_framework import serializers

from equipment.models import Equipment


class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = '__all__'
