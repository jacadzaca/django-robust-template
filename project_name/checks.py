# noqa
# based on: https://gist.github.com/hakib/e2e50d41d19a6984dc63bd94580c8647
import ast
import inspect

import django
from django.core import checks
from django.core.checks import Error, Warning
from django.core.exceptions import FieldDoesNotExist
from django.db.models import (
    CharField,
    ForeignKey,
    BooleanField,
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
            is_default_value_defined = False
            is_null_explicitly_defined = False
            is_blank_explicitly_defined = False
            is_max_length_explicitly_defined = False
            is_default_database_value_defined = False
            is_related_name_defined = False
            is_related_query_name_defined = False
            for argument in node.value.keywords:
                if argument.arg == 'verbose_name':
                    is_verbose_name_defined = True
                elif argument.arg == 'db_comment':
                    is_db_comment_defined = True
                elif argument.arg == 'null':
                    is_null_explicitly_defined = True
                elif argument.arg == 'blank':
                    is_blank_explicitly_defined = True
                elif argument.arg == 'max_length':
                    is_max_length_explicitly_defined = True
                elif argument.arg == 'default':
                    is_default_value_defined = True
                elif argument.arg == 'db_default':
                    is_default_database_value_defined = True
                elif argument.arg == 'related_name':
                    is_related_name_defined = True
                elif argument.arg == 'related_query_name':
                    is_related_query_name_defined  = True

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
            # `null` has no effect on ManyToManyField
            if (not is_null_explicitly_defined) and (not isinstance(field, ManyToManyField)):
                problems.append(
                    Error(
                        'Field does not explicitly set the `null` argument',
                        hint=(
                            f'Set explicitly either `null=False` or `null=True` '
                            f'on `{model.__module__}.{model.__name__}.{field.name}`. '
                            'See https://docs.djangoproject.com/en/{{ docs_version }}/ref/models/fields/#null'
                        ),
                        obj=field,
                        id='django_robust_template.J003',
                    ),
                )
            if not is_blank_explicitly_defined:
                problems.append(
                    Error(
                        'Field dose not explicitly set the `blank` argument',
                        hint=(
                            f'Set explicitly either `blank=False` or `blank=True` '
                            f'on `{model.__module__}.{model.__name__}.{field.name}` '
                            'See https://docs.djangoproject.com/en/{{ docs_version }}/ref/models/fields/#blank'
                        ),
                        obj=field,
                        id='django_robust_template.J004',
                    ),
                )
            if (not is_max_length_explicitly_defined) and (isinstance(field, CharField)):
                problems.append(
                    Warning(
                        'CharField dose not explicitly set the `max_length` argument',
                        hint=(
                            f'Consider setting `max_length` argument explicitly on `{model.__module__}.{model.__name__}.{field.name}`. '
                            'Not setting it means that the value has unlimited length, which is controversial design. '
                            'See https://docs.djangoproject.com/en/{{ docs_version }}/ref/models/fields/#django.db.models.CharField.max_length'
                        ),
                        obj=field,
                        id='django_robust_template.J005',
                    ),
                )
            if (not is_default_value_defined) and (isinstance(field, BooleanField)):
                problems.append(
                    Warning(
                        'BooleanField does not explicitly set the `default` argument',
                        hint=(
                            f'Consider setting the either `default=False` or `default=True` explicitly on `{model.__module__}.{model.__name__}.{field.name}`. '
                            'Not setting `default` on a BooleanField means that the field can contain NULL values, which *might* not '
                            'make sense. See https://docs.djangoproject.com/en/{{ docs_version }}/ref/models/fields/#booleanfield'
                        ),
                        obj=field,
                        id='django_robust_template.J007',
                    ),
                )
            if is_default_value_defined and (not is_default_database_value_defined):
                problems.append(
                    Warning(
                        'Field dose define a default value but no `db_default` value',
                        hint=(
                            f'Consider setting both the default value and the `db_default` value on `{model.__module__}.{model.__name__}.{field.name}`. '
                            'Direct inserts on the database level can leave the field NULL, which might break the expectations to which the data '
                            'should conform to when accessing it. See https://docs.djangoproject.com/en/{{ docs_version }}/ref/models/fields/#db-default'
                        ),
                        obj=field,
                        id='django_robust_template.J008',
                    )
                )
            if (not is_related_name_defined) and isinstance(field, (ForeignKey, ManyToManyField)):
                problems.append(
                    Error(
                        'Field dose not explicitly define the `related_name` argument',
                        hint=(
                            f'Please set a value for the `related_name` of '
                            f'`{model.__module__}.{model.__name__}.{field.name}`. '
                            'See https://docs.djangoproject.com/en/{{ docs_version }}/ref/models/fields/#django.db.models.ForeignKey.related_name'
                        ),
                        obj=field,
                        id='django_robust_template.J009',
                    ),
                )
            if (not is_related_query_name_defined) and isinstance(field, (ForeignKey, ManyToManyField)):
                problems.append(
                    Error(
                        'Field dose not explicitly define the `related_query_name` argument',
                        hint=(
                            f'Please set a value for the `related_query_name` of '
                            f'`{model.__module__}.{model.__name__}.{field.name}`. See '
                            'https://docs.djangoproject.com/en/{{ docs_version }}/ref/models/fields/#django.db.models.ForeignKey.related_query_name'
                        ),
                        obj=field,
                        id='django_robust_template.J010',
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

