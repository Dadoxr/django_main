import random
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, FormView, ListView, UpdateView
from django.conf import settings

from users.forms import EmailConfirmationForm, MyUserCreationForm, MyUserChangeForm
from users.models import User


class RegisterView(CreateView):
    model = User
    form_class = MyUserCreationForm
    template_name = "users/register.html"
    success_url = reverse_lazy("users:email_confirmation")

    def form_valid(self, form):
        self.object = form.save()
        code = "".join([str(random.randint(0, 9)) for _ in range(6)])
        self.object.confirmation_code = code
        self.object.save()

        send_mail(
            subject="Подтверждение почты РАЗОШЛИ",
            message=f"Ваш проверочный код: {code}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[self.object.email],
        )

        return super().form_valid(form)


class EmailConfirmationView(FormView):
    form_class = EmailConfirmationForm
    template_name = "users/email_confirmation.html"
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        confirmation_code = form.cleaned_data["confirmation_code"]
        print(confirmation_code)
        user = User.objects.get(confirmation_code=confirmation_code)
        user.confirmation_code = None
        user.save()
        return super().form_valid(form)


class ProfileView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = "users/profile.html"
    form_class = MyUserChangeForm
    success_url = reverse_lazy("users:profile")
    extra_context = {
        "site_name": settings.SITE_NAME,
        "title": "Настройка профиля",
        "description": "Здесь вы можете изменять настройки профиля",
    }

    def get_object(self, queryset=None):
        return self.request.user


class UserListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = User
    permission_required = 'users.view_user'
    template_name = "users/list.html"
    extra_context = {
        "site_name": settings.SITE_NAME,
        "title": "Управление сообщениями",
        "description": "Здесь вы можете изменять сообщения и удалять их",
    }

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(is_superuser=False, is_staff=False)



@login_required
def change_active(request, pk):
    user_object = User.objects.get(pk=pk)
    if request.user.is_staff and not user_object.is_superuser and not user_object.is_staff:
        if user_object.is_active:
            user_object.is_active = False
        else:
            user_object.is_active = True
        user_object.save()
    return redirect(reverse('users:list'))
