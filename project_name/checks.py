# based on: https://gist.github.com/hakib/e2e50d41d19a6984dc63bd94580c8647
import ast
import inspect

import django.apps
from django.core import checks
from django.core.checks import Error
from django.core.exceptions import FieldDoesNotExist


def check_all_models_fields_have_verbose_name(model):
    model_source = inspect.getsource(model)
    model_ast = ast.parse(model_source)

    for node in model_ast.body[0].body:
        # fields are defined as class level 
        # attributes we can ignore all other
        # types of nodes
        if not isinstance(node, ast.Assign):
            continue

        # we only care about top-level attributes
        if len(node.targets) != 1:
            continue

        # model fields will have a Name target
        if not isinstance(node.targets[0], ast.Name):
            continue

        field_name = node.targets[0].id
        try:
            # only fields will be in the model's Meta
            field = model._meta.get_field(field_name)
        except FieldDoesNotExist:
            continue

        verbose_name = None
        for argument in node.value.keywords:
            if argument.arg == 'verbose_name':
                # the field has `verbose_name` argument
                verbose_name = kw
                break
        if verbose_name is None:
            yield Error(
                'Field has no verbose name',
                hint=f"Set verbose_name on {model.__module__}.{model.__name__} field `{field.name}`",
                obj=field,
                id='J001',
            )


@checks.register(checks.Tags.models)
def check_each_model_field_has_verbose_name(app_configs, **kwargs):
    problems = []
    for app in django.apps.apps.get_app_configs():
        # skip third party apps
        if app.path.find('site-packages') > -1:
            continue

        for model in app.get_models():
            for check_message in check_all_models_fields_have_verbose_name(model):
                problems.append(check_message)

    return problems


