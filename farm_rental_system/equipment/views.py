from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from utils.ApiResponse import ApiResponse

from .models import Equipment
from .serializers import EquipmentSerializer
from rest_framework import status

from utils.decorators import allowed_users


class EquipmentView(viewsets.ModelViewSet):
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer

    # permission_classes = [IsAuthenticated]  # Restrict access to authenticated users
    def list_equipment(self, request, *args, **kwargs):
        response = ApiResponse()
        data = list(Equipment.objects.all().values())
        response.setStatusCode(status.HTTP_200_OK)
        response.setMessage("Found")
        response.setEntity(data)
        return Response(response.toDict(), status=response.status)

    def create_equipment(self, request):
        """Create new equipment."""
        serializer = EquipmentSerializer(data=request.data)
        if serializer.is_valid():
            # Save without the owner field since it doesn't exist in the model
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve_equipment(self, request, pk=None):
        """Get details of a specific piece of equipment."""
        try:
            equipment = Equipment.objects.get(pk=pk)
            serializer = EquipmentSerializer(equipment)
            return Response(serializer.data)
        except Equipment.DoesNotExist:
            return Response({"error": "Equipment not found"}, status=status.HTTP_404_NOT_FOUND)

    def update_equipment(self, request, pk=None):
        """Update equipment details."""
        try:
            equipment = Equipment.objects.get(pk=pk)
        except Equipment.DoesNotExist:
            return Response({"error": "Equipment not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = EquipmentSerializer(equipment, data=request.data, partial=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy_equipment(self, request, pk=None):
        """Delete a specific piece of equipment."""
        try:
            equipment = Equipment.objects.get(pk=pk)
            equipment.delete()
            return Response({"message": "Equipment deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Equipment.DoesNotExist:
            return Response({"error": "Equipment not found"}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['get'], url_path='filter-by-location-category')
    # @allowed_users(allowed_roles=["admin", "farmer"])
    def filter_by_location_and_category(self, request):
        """Filter equipment by location and category."""
        location = request.query_params.get('location', None)
        category = request.query_params.get('category', None)

        # Filter by location and category if provided
        if location and category:
            filtered_equipment = Equipment.objects.filter(location__icontains=location, category=category)
        # Filter by location if only location is provided
        elif location:
            filtered_equipment = Equipment.objects.filter(location__icontains=location)
        # Filter by category if only category is provided
        elif category:
            filtered_equipment = Equipment.objects.filter(category=category)
        else:
            return Response({"error": "At least one filter parameter (location or category) is required."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Serialize the filtered queryset
        serializer = EquipmentSerializer(filtered_equipment, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['patch'], url_path='set-price')
    # @allowed_users(allowed_roles=["admin", "farmer"])
    def set_price(self, request, pk=None):
        """Custom endpoint to set or update the price of equipment."""
        try:
            # Retrieve the equipment by its primary key (pk)
            equipment = Equipment.objects.get(pk=pk)
        except Equipment.DoesNotExist:
            return Response({"error": "Equipment not found."}, status=status.HTTP_404_NOT_FOUND)

        # Check if 'price_per_day' is in the request data
        price = request.data.get('price_per_day', None)
        if price is None:
            return Response({"error": "Price per day is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Validate the price (must be positive and greater than zero)
        try:
            price = float(price)
            if price <= 0:
                return Response({"error": "Price must be greater than zero."}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError:
            return Response({"error": "Invalid price format."}, status=status.HTTP_400_BAD_REQUEST)

        # Update the price of the equipment
        equipment.price_per_day = price
        equipment.save()

        # Return the updated equipment data
        serializer = EquipmentSerializer(equipment)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['patch'], url_path='update-availability')
    # @allowed_users(allowed_roles=["admin", "farmer"])
    def update_availability(self, request, pk=None):
        """Custom endpoint to update the availability of equipment."""
        try:
            equipment = Equipment.objects.get(pk=pk)
        except Equipment.DoesNotExist:
            return Response({"error": "Equipment not found."}, status=status.HTTP_404_NOT_FOUND)

        # Check if 'availability' is in the request data
        availability = request.data.get('availability', None)
        if availability is None:
            return Response({"error": "Availability status is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Validate the availability status (must be a boolean: true or false)
        if not isinstance(availability, bool):
            return Response({"error": "Invalid availability status. It must be a boolean."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Update the availability status of the equipment
        equipment.availability = availability
        equipment.save()

        # Return the updated equipment data
        serializer = EquipmentSerializer(equipment)
        return Response(serializer.data, status=status.HTTP_200_OK)
