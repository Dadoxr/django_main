from django.contrib.auth.views import LoginView,LogoutView
from users.views import RegisterView, ProfileView, EmailConfirmationView, UserListView, change_active
from django.urls import path

from users.apps import UsersConfig


app_name = UsersConfig.name

urlpatterns = [
    path('', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('register/email_confirmation', EmailConfirmationView.as_view(), name='email_confirmation'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('list/', UserListView.as_view(), name='list'),
    path('change_active/<int:pk>', change_active, name='change_active'),
]