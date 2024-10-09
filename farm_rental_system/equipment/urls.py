from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EquipmentView

# Create a router and register the EquipmentViewSet
router = DefaultRouter()
router.register(r'', EquipmentView, basename='')

urlpatterns = [
    path('list/', EquipmentView.as_view({'get': 'list'}), name='list'),
    path('create/', EquipmentView.as_view({'post': 'create'}), name='create'),
    path('update/<int:pk>', EquipmentView.as_view({'put': 'update'}), name='update'),
    path('destroy/<int:pk>', EquipmentView.as_view({'delete': 'destroy'}), name='destroy'),

    path('filter/location/category/',
         EquipmentView.as_view({'get': 'filter_by_location_and_category'}),
         name='filter_by_location_category'),
    path('update/availability/<int:pk>/',
         EquipmentView.as_view({'patch': 'update_availability'}),
         name='update_availability'),
    path('set/price/<int:pk>/',
         EquipmentView.as_view({'patch': 'set_price'}),
         name='set_price'),

]
