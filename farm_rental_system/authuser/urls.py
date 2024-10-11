from django.urls import path

from .views import AuthUSer

urlpatterns = [
    path('login/', AuthUSer.as_view({'post': 'authUser'}), name='authuser'),
    path('sendotp/', AuthUSer.as_view({'post': 'sendUserdOTP'}), name='sendOTP'),
    path('verifyotp/', AuthUSer.as_view({'post': 'verifyUserOTP'}), name='verifyOTP'),
    path('resetpassword/', AuthUSer.as_view({'post': 'resetUserpassword'}), name='resetpassword'),
]
