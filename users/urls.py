from django.urls import path

from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)

from users.forms import (
    {{ camel_case_project_name}}UserLoginForm,
    {{ camel_case_project_name}}UserPasswordResetForm,
    {{ camel_case_project_name}}UserPasswordResetConfirmForm,
)


urlpatterns = [
    path(
        'login/',
        LoginView.as_view(
            authentication_form={{ camel_case_project_name}}UserLoginForm,
        ),
        name='login',
    ),
    path(
        'logout/',
        LogoutView.as_view(),
        name='logout',
    ),
    path(
        'password_reset/',
        PasswordResetView.as_view(
            form_class={{ camel_case_project_name}}UserPasswordResetForm,
        ),
        name='password_reset',
    ),
    path(
        'password_reset/done/',
        PasswordResetDoneView.as_view(),
        name='password_reset_done',
    ),
    path(
        'password_reset/<uidb64>/<token>/',
        PasswordResetConfirmView.as_view(
            form_class={{ camel_case_project_name}}UserPasswordResetConfirmForm,
        ),
        name='password_reset_confirm',
    ),
    path(
        'password_reset/complete/',
        PasswordResetCompleteView.as_view(),
        name='password_reset_complete',
    ),
]

