"""
URL configuration for farm_rental_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from equipment import views as equipment_views
from bookings import views as bookings_views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

schema_view = get_schema_view(
    openapi.Info(
        title="FarmEquipment",
        default_version='v1',
        description="API documentation for LibraTech",
    ),
    # public=True,
    # permission_classes=(permissions.AllowAny,)
)


urlpatterns = [
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('', equipment_views.home, name='home'),
    path('admin/', admin.site.urls),
    path('equipment/', equipment_views.equipment_list, name='equipment_list'),
    path('equipment/<int:pk>/', equipment_views.equipment_detail, name='equipment_detail'),
    path('booking/create/<int:equipment_id>/', bookings_views.create_booking, name='create_booking'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


