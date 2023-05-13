from django.urls import path

from .views import *

urlpatterns = [
    path('authorization/', authorization, name='authorization'),
    path('authorization/password_recovery/', password_recovery, name='password_recovery'),
    path('registration/', registerUser, name='registration'),

    path('logout/', user_logout, name='logout')
]
