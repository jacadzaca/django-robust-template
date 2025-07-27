from django.contrib.auth.forms import (
    UserChangeForm,
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

