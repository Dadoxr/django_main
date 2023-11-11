import random
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView, UpdateView
from django.conf import settings

from users.forms import EmailConfirmationForm, MyUserCreationForm, MyUserChangeForm
from users.models import User


class RegisterView(CreateView):
    model = User
    form_class = MyUserCreationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:email_confirmation')

    def form_valid(self, form):
        self.object = form.save()
        code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        self.object.confirmation_code = code
        self.object.save()
        
        send_mail(
            subject='Подтверждение почты РАЗОШЛИ',
            message=f'Ваш проверочный код: {code}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[self.object.email]
        )

        return super().form_valid(form)

class EmailConfirmationView(FormView):
    form_class = EmailConfirmationForm
    template_name = 'users/email_confirmation.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        confirmation_code = form.cleaned_data['confirmation_code']
        print(confirmation_code)
        user = User.objects.get(confirmation_code=confirmation_code)
        user.confirmation_code = None
        user.save()
        return super().form_valid(form)


class ProfileView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'users/profile.html'
    form_class = MyUserChangeForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user
    
