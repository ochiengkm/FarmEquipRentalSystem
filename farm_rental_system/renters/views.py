from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response

from renters.models import Renters
from renters.serializers import RentersSerializer
from utils.ApiResponse import ApiResponse


# Create your views here.

class RentersView(viewsets.ModelViewSet):
    queryset = Renters.objects.all()
    serializer_class = RentersSerializer

    def create(self, request, *args, **kwargs):
        response = ApiResponse()
        rentersData = RentersSerializer(data=request.data)

        if not rentersData.is_valid():
            status_code = status.HTTP_400_BAD_REQUEST
            print(rentersData.errors)  # Log validation errors
            return Response({"message": "Please fill in your details correctly", "status": status_code, "errors": rentersData.errors}, status_code)


        email = request.data.get("email")

        existing_renter = Renters.objects.filter(email=email).first()

        if existing_renter:
            status_code = status.HTTP_400_BAD_REQUEST
            return Response({"message": "Borrower already exists", "status": status_code}, status_code)

        renter = rentersData.save()

        response.setStatusCode(status.HTTP_201_CREATED)
        response.setMessage("Renter created")
        response.setEntity(RentersSerializer(renter).data)  # Return saved renter data
        return Response(response.toDict(), status=response.status)

    def list(self, request, *args, **kwargs):
        response = ApiResponse()
        data = list(Renters.objects.all().values())
        response.setStatusCode(status.HTTP_200_OK)
        response.setMessage("Found")
        response.setEntity(data)
        return Response(response.toDict(), status=response.status)

    def update(self, request, *args, **kwargs):
        renter_instance = get_object_or_404(Renters, id=kwargs['pk'])
        renter_serializer = RentersSerializer(renter_instance, data=request.data, partial=True)

        if renter_serializer.is_valid():
            renter_serializer.save()
            status_code = status.HTTP_200_OK
            return Response({"message": "Renters data updated successfully", "status": status_code}, status_code)
        else:
            status_code = status.HTTP_400_BAD_REQUEST
            return Response({"message": "Renters data not valid", "status": status_code}, status_code)

    def destroy(self, request, *args, **kwargs):
        renterData = Renters.objects.filter(id=kwargs['pk'])
        if renterData:
            renterData.delete()
            status_code = status.HTTP_200_OK
            return Response({"message": "Renters data deleted successfully", "status": status_code}, status_code)
        else:
            status_code = status.HTTP_400_BAD_REQUEST
            return Response({"message": "Renters data not found", "status": status_code}, status_code)

