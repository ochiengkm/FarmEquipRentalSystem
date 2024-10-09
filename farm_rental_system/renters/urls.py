from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import RentersView

router = DefaultRouter()
router.register(r'', RentersView, basename='')

urlpatterns = [
    path('create', RentersView.as_view({'post': 'create'}), name='create'),
    path('list', RentersView.as_view({'get': 'list'}), name='list'),
    path('update/<int:pk>', RentersView.as_view({'put': 'update'}), name='update'),
    path('delete/<int:pk>', RentersView.as_view({'delete': 'destroy'}), name='delete'),
    path('deactivate/<str:str>', RentersView.as_view({'post': 'deactivate'}), name='deactivate')

]
