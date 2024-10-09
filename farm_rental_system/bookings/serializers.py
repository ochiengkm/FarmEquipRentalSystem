from rest_framework import serializers
from .models import Bookings, Equipment, Renters


class BookingsSerializer(serializers.ModelSerializer):
    equipment_name = serializers.SlugRelatedField(slug_field='name', queryset=Equipment.objects.all(),
                                                  source='equipment')
    renter_email = serializers.SlugRelatedField(slug_field='email', queryset=Renters.objects.all(),
                                                source='renters')

    class Meta:
        model = Bookings
        fields = ['renter_email', 'equipment_name', 'reservationDate', 'pickupDate']
        extra_kwargs = {
            'reservationDate': {'read_only': True}
        }
