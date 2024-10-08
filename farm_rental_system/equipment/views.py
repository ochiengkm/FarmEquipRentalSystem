from django.shortcuts import render
from .models import Equipment


# Create your views here.
def home(request):
    return render(request, 'home.html')


def equipment_list(request):
    equipment = Equipment.objects.filter(availability=True)
    return render(request, 'equipment/equipment_list.html', {'equipment': equipment})


def equipment_detail(request, pk):
    equipment = Equipment.objects.get(id=pk)
    return render(request, 'equipment/equipment_detail.html', {'equipment': equipment})
