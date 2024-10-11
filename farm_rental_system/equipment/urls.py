from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EquipmentView

# Create a router and register the EquipmentViewSet
router = DefaultRouter()
router.register(r'', EquipmentView, basename='')

urlpatterns = [
    path('list/', EquipmentView.as_view({'get': 'list_equipment'}), name='list'),
    path('retrieve', EquipmentView.as_view({'get': 'retrieve_equipment'}), name='retrieve'),
    path('create/', EquipmentView.as_view({'post': 'create_equipment'}), name='create'),
    path('update/<int:pk>', EquipmentView.as_view({'put': 'update_equipment'}), name='update'),
    path('destroy/<int:pk>', EquipmentView.as_view({'delete': 'destroy_equipment'}), name='destroy'),

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
