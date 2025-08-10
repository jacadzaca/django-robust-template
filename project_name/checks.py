# noqa
# based on: https://gist.github.com/hakib/e2e50d41d19a6984dc63bd94580c8647
import ast
import inspect

import django
from django.core import checks
from django.core.checks import Error, Warning
from django.core.exceptions import FieldDoesNotExist
from django.db.models import (
    ManyToManyField,
)


def might_be_field_assignment(node) -> bool:
    '''
    a field assigment field must:
        1. be a Assign node
        2. be top-level on class
        3. have a `Name`` target
    '''
    return (
        isinstance(node, ast.Assign)
        and len(node.targets) == 1
        and isinstance(node.targets[0], ast.Name)
    )


def check_model(model) -> list[Error]:
    problems = []

    model_source = inspect.getsource(model)
    model_ast = ast.parse(model_source)
    for node in model_ast.body[0].body:
        if might_be_field_assignment(node):
            field_name = node.targets[0].id
            try:
                # only fields will be in the model's Meta
                field = model._meta.get_field(field_name)
            except FieldDoesNotExist:
                continue

            is_db_comment_defined = False 
            is_verbose_name_defined = False
            for argument in node.value.keywords:
                if argument.arg == 'verbose_name':
                    is_verbose_name_defined = True
                elif argument.arg == 'db_comment':
                    is_db_comment_defined = True

            if not is_verbose_name_defined:
                problems.append(
                    Error(
                        'Field has no verbose name',
                        hint=f"Set verbose_name on `{model.__module__}.{model.__name__}.{field.name}`",
                        obj=field,
                        id='django_robust_template.J001',
                    ),
                )
            if (not is_db_comment_defined) and (not isinstance(field, ManyToManyField)):
                problems.append(
                    Error(
                        'Field has no database comment',
                        hint=(
                            f'Set `db_comment` on `{model.__module__}.{model.__name__}.{field.name}`'
                            'See https://docs.djangoproject.com/en/{{ docs_version }}/ref/models/fields/#db-comment'
                        ),
                        obj=field,
                        id='django_robust_template.J002',
                    ),
                )
            elif is_db_comment_defined:
                if not field.db_comment.isascii():
                    problems.append(
                        Warning(
                            'Field has non-ascii `db_comment`',
                            hint=(
                                'Consider removing non-ascii (e.g. diacritics) from the db_comment. '
                                'Some database backends (e.g. Oracle) can have problems with handling non-ascii comments.'
                            ),
                            obj=field,
                            id='django_robust_template.J006'
                        ),
                    )

    return problems


@checks.register(checks.Tags.models)
def check_first_party_models(
    app_configs,
    **kwargs,
) -> list[Error]:
    problems = []
    for app in django.apps.apps.get_app_configs():
        # skip third party apps
        if app.path.find('site-packages') > -1:
            continue

        for model in app.get_models():
            problems_with_model = check_model(model)
            problems += problems_with_model

    return problems

