from django.shortcuts import render, redirect
from .models import Booking
from equipment.models import Equipment
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from datetime import datetime


# Create your views here.
@login_required
def create_booking(request, equipment_id):
    equipment = Equipment.objects.get(id=equipment_id)

    if request.method == 'POST':
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        total_price = equipment.rental_price * (
                    datetime.strptime(end_date, '%Y-%m-%d') - datetime.strptime(start_date, '%Y-%m-%d')).days

        booking = Booking.objects.create(
            equipment=equipment,
            user=request.user,
            start_date=start_date,
            end_date=end_date,
            total_price=total_price
        )
        return redirect('booking_confirmation', booking_id=booking.id)
    return render(request, 'bookings/create_booking.html', {'equipment': equipment})
