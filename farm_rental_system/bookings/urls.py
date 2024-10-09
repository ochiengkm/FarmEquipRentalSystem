from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import BookingsView

router = DefaultRouter()
router.register(r'', BookingsView, basename='')

urlpatterns = [
    # path('', include(router.urls)),
    path('book/equipment/', BookingsView.as_view({'post': 'book_equipment'}), name='book_equipment'),
    path('booking/list/', BookingsView.as_view({'get': 'reservation_list'}), name='reservation_list')
]
