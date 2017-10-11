from django.conf.urls import url

from .views import (
    UserLoginView,
    UserLogoutView,
    RegisterView,
    UserProfileView,
    UpdateProfileView,
    UpdatePasswordView
)

urlpatterns = [
    url(r'^login/$', UserLoginView.as_view(), name='user_login'),
    url(r'^logout/$', UserLogoutView.as_view(), name='user_logout'),
    url(r'^registration/$', RegisterView.as_view(), name='register'),
    url(r'^profile/$', UserProfileView.as_view(), name='user_profile'),
    url(r'^profile/edit/$', UpdateProfileView.as_view(), name='edit_profile'),
    url(r'^profile/editpassword/$', UpdatePasswordView.as_view(), name='edit_password'),
]