from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import {{ camel_case_project_name }}User
from users.forms import (
    {{ camel_case_project_name }}UserChangeForm,
    {{ camel_case_project_name }}UserCreationForm,
)


@admin.register({{ camel_case_project_name }}User)
class {{ camel_case_project_name }}UserAdmin(UserAdmin):
    add_form = {{ camel_case_project_name }}UserCreationForm
    form = {{ camel_case_project_name }}UserChangeForm 
    model = {{ camel_case_project_name }}User

    list_display = [
        'user_id',
        'first_name',
        'last_name',
        'email',
        'username',
        'is_staff',
        'is_active',
        'last_login',
        'date_joined',
    ]

    list_editable = [
        'first_name',
        'last_name',
        'email',
        'is_staff',
        'is_active',
    ]

    def user_id(self, user: {{ camel_case_project_name }}User) -> str:
        return f'#{user.pk}'
    user_id.short_descritpion = 'ID'

