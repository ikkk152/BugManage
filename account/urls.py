from django.urls import path

from .views import Register, SendSms, Login

urlpatterns = [
    path('register/', Register.as_view()),
    path('send_sms/', SendSms.as_view()),
    path('login/', Login.as_view()),
]
