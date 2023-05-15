from django.urls import path
from .views import *
from django.contrib.auth.views import (
PasswordResetView,
PasswordResetDoneView,
PasswordResetConfirmView,
PasswordResetCompleteView
)
urlpatterns = [
    path('profile/<uuid:pk>/', ProfileView.as_view(), name='profile'),
    path('regions-by-country/', regions_by_country, name='regions'),
    path('password-reset/', PasswordResetView.as_view(template_name='user/password_reset.html'),name='password-reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(template_name='user/password_reset_done.html'),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='user/password_reset_confirm.html'),name='password_reset_confirm'),
    path('password-reset-complete/',PasswordResetCompleteView.as_view(template_name='user/password_reset_complete.html'),name='password_reset_complete'),


]