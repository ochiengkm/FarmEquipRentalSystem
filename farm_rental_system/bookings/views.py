from datetime import datetime, timedelta

from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response


from equipment.models import Equipment
from bookings.models import Bookings
from bookings.serializers import BookingsSerializer
from renters.models import Renters
from utils.ApiResponse import ApiResponse


# Create your views here.

class BookingsView(viewsets.ModelViewSet):
    queryset = Bookings.objects.all()
    serializer_class = BookingsSerializer

    def reservation_list(self, request, *args, **kwargs):
        response = ApiResponse()
        data = Bookings.objects.all()

        serializer = BookingsSerializer(data, many=True)
        serialized_data = serializer.data

        response.setStatusCode(status.HTTP_200_OK)
        response.setMessage("Found")
        response.setEntity(serialized_data)
        return Response(response.toDict(), status=response.status)

    @action(detail=False, methods=['post'])
    def book_equipment(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        equipment_name = serializer.validated_data['equipment'].name
        renter_email = serializer.validated_data['renters'].email

        # Get the equipment instance by name
        try:
            equipment = Equipment.objects.get(name=equipment_name)
        except Equipment.DoesNotExist:
            return Response({'error': 'Equipment not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Get the renter instance by email
        try:
            renter = Renters.objects.get(email=renter_email)
        except Renters.DoesNotExist:
            return Response({'error': 'Renter not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Check if the equipment is available for reservation
        if equipment.status != 'available':
            return Response({'error': 'Equipment is not available for reservation.'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Check if a reservation with the same renter and equipment already exists
        if Bookings.objects.filter(renters=renter, equipment=equipment).exists():
            return Response({'error': 'Booking already exists for this renter and equipment.'},
                            status=status.HTTP_400_BAD_REQUEST)

        # Create the reservation
        booking = Bookings.objects.create(
            renters=renter,
            equipment=equipment,
            pickupDate=serializer.validated_data['pickupDate']
        )

        # Update the equipment status to 'booked'
        equipment.status = 'booked'
        equipment.save()

        return Response({'message': 'Equipment booked successfully.', 'data': BookingsSerializer(booking).data},
                        status=status.HTTP_201_CREATED)
