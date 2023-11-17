from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from users.models import User


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            "email",
            "password1",
            "password2",
        )


class MyUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = (
            "email",
            "first_name",
            "last_name",
            "comment",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password"].widget = forms.HiddenInput()


class EmailConfirmationForm(forms.Form):
    confirmation_code = forms.CharField(max_length=6)

    def clean_confirmation_code(self):
        confirmation_code = self.cleaned_data.get("confirmation_code")
        if not User.objects.filter(confirmation_code=confirmation_code).exists():
            raise forms.ValidationError("Неверный код подтверждения.")
        return confirmation_code
