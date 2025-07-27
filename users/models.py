from django.contrib.auth.models import AbstractUser


class {{ camel_case_project_name }}User(AbstractUser):
    class Meta:
        default_permissions = ()

        db_table = '{{ project_name|upper }}_USERS'
        db_table_comment = 'Table with {{ camel_case_project_name }} users'

        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self) -> str:
        full_name = self.get_full_name()
        return full_name or self.username

    def __repr__(self) -> str:
        return f'{self.username} ({self.email})'

