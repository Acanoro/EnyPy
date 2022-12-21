from django.contrib.auth import views as auth_views
from django.urls import path

from .views import *

urlpatterns = [
    path('authorization/', authorization, name='authorization'),
    path('authorization/password_recovery/', password_recovery, name='password_recovery'),
    path('registration/', registerUser, name='registration'),

    path('logout/', user_logout, name='logout'),

    # restore password urls
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
