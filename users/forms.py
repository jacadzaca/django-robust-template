from django.forms import (
    CharField,
    TextInput,
    EmailField,
    EmailInput,
    PasswordInput,
)
from django.contrib.auth.forms import (
    UsernameField,
    UserChangeForm,
    SetPasswordForm,
    PasswordResetForm,
    AuthenticationForm,
    AdminUserCreationForm,
)

from users.models import {{ camel_case_project_name }}User

class {{ camel_case_project_name }}UserCreationForm(AdminUserCreationForm):
    class Meta:
        model = {{ camel_case_project_name }}User
        fields = ('username', 'email')


class {{ camel_case_project_name }}UserChangeForm(UserChangeForm):
    class Meta:
        model = {{ camel_case_project_name }}User
        fields = ('username', 'email')


class {{ camel_case_project_name }}UserLoginForm(AuthenticationForm):
    username = UsernameField(
        widget=TextInput(
            attrs={
                'placeholder': 'Enter your username here',
            },
        ),
    )

    password = CharField(
        widget=PasswordInput(
            attrs={
                'placeholder': 'Enter your password here',
            },
        ),
    )


class {{ camel_case_project_name}}UserPasswordResetForm(PasswordResetForm):
    email = EmailField(
        max_length=254,
        widget=EmailInput(
            attrs={
                'autocomplete': 'email',
                'placeholder': 'Enter your email address here',
            },
        ),
    )


class {{ camel_case_project_name}}UserPasswordResetConfirmForm(SetPasswordForm):
    new_password1 = CharField(
        label="New password",
        strip=False,
        help_text=(
            '<ul><li>Your password can’t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can’t be a commonly used password.</li><li>Your password can’t be entirely numeric.</li></ul>'
        ),
        widget=PasswordInput(
            attrs={
                'placeholder': 'Enter your new password here',
            },
        ),
    )

    new_password2 = CharField(
        label="Confirm new password",
        strip=False,
        help_text='Enter the same password as before, for verification',
        widget=PasswordInput(
            attrs={
                'placeholder': 'Enter your new password again here',
            },
        ),
    )


