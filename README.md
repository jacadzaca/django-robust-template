# django-robust-template
A simple django project template that I believe is a good starting point
for a project that is a small/medium internal tools (e.g a dashboard used by your department).
This template includes:
 - boilerplate for django password authentication
 - boilerplate for configuring django error pages
 - boilerplate for [django-jazzmin](https://django-jazzmin.readthedocs.io/) configuration
 - [Github Actions](https://docs.github.com/en/actions) for running tests
 using [pytest](https://docs.pytest.org/en/stable/), type checking using [mypy](https://www.mypy-lang.org/), linting with [ruff](https://docs.astral.sh/ruff/) checking whether the program's version
 was bumped
 - a starting point for the UI
 - a Docker image definition that runs the application via [bjoern](https://github.com/jonashaag/bjoern)
 - most of [django settings](https://docs.djangoproject.com/en/{{ docs_version }}/ref/settings/) you'd like to define via environment
 variables exposed
 - [Whitenoise](https://whitenoise.readthedocs.io/en/latest/) for django configured
 - sqlite configured such that the datestimes are stored in the correct timezone
 - useful [django system checks](#list-of-custom-django-system-checks)

# Usage
I believe that it's best to fork this repository and modify the template slightly
to your liking. You can also use this repository as a template as such:

```bash
PROJECT_NAME="<INSERT YOUR PROJECT NAME HERE>"
PROJECT_DESCRIPTION="<INSERT A SHORT PROJECT DESCRIPTION HERE>"
MAINTAINER_EMAIL="<INSERT THE PROJECT'S MAINTAINER EMAIL HERE>"
COMPANY_DOMAIN="<INSERT THE EMAIL DOMAIN OF YOUR COMPANY HERE>"
COMPANY_NAME="<INSERT YOUR COMPANY NAME HERE>"

python -m venv venv \
    && source venv/bin/activate \
    && pip install django django-jazzmin whitenoise pytest pytest-django pytest-xdist coverage mypy django-stubs ruff bjoern \
    && pip freeze > requirements.txt

django-admin startproject --template "https://github.com/jacadzaca/django-robust-template/archive/refs/heads/master.zip" --name "Dockerfile" --name "pyproject.toml"  --name "CHANGELOG.md" --exclude ".git" --name "README.md" "${PROJECT_NAME}" .

sed -ie "s/{{ project_name }}/$PROJECT_NAME/g" .github/workflows/check_version_bumped.yml
sed -ie "s/{{ project_name }}/$PROJECT_NAME/g" .github/workflows/check_enviroment_variables_included_in_readme.yml
sed -ie "s/Your application's description/$PROJECT_DESCRIPTION/g" Dockerfile
sed -ie "s/Your company/$COMPANY_NAME/g" Dockerfile
sed -ie "s/your.email@example.com/$MAINTAINER_EMAIL/g" Dockerfile
sed -ie "s/project_name/$PROJECT_NAME/g" templates/base.html
sed -ie "s/your.name@example.com/MAINTAINER_EMAIL/g" $PROJECT_NAME/settings.py
sed -ie "s/example.com/COMPANY_DOMAIN/g" $PROJECT_NAME/settings.py
```

or using PowerShell:

```pwershell
$PROJECT_NAME = "<INSERT YOUR PROJECT NAME HERE>"
$PROJECT_DESCRIPTION = "<INSERT A SHORT PROJECT DESCRIPTION HERE>"
$MAINTAINER_EMAIL = "<INSERT THE PROJECT'S MAINTAINER EMAIL HERE>"
$COMPANY_DOMAIN = "<INSERT THE EMAIL DOMAIN OF YOUR COMPANY HERE>"
$COMPANY_NAME = "<INSERT YOUR COMPANY NAME HERE>"

python -m venv venv
& "venv/Scripts/Activate.ps1"

pip install django django-jazzmin whitenoise pytest pytest-django pytest-xdist coverage mypy django-stubs ruff bjoern

pip freeze > requirements.txt

django-admin startproject --template "https://github.com/jacadzaca/django-robust-template/archive/refs/heads/master.zip" `
    --name "Dockerfile" `
    --name "pyproject.toml" `
    --name "CHANGELOG.md" `
    --name "README.md" `
    --exclude ".git" `
    $PROJECT_NAME .

(gc ".github/workflows/check_version_bumped.yml") -replace "{{ project_name }}", $PROJECT_NAME | Set-Content ".github/workflows/check_version_bumped.yml"
(gc "Dockerfile") -replace "Your application's description", $PROJECT_DESCRIPTION `
                 -replace "Your company", $COMPANY_NAME `
                 -replace "your.email@example.com", $MAINTAINER_EMAIL | Set-Content "Dockerfile"
(gc "templates/base.html") -replace "project_name", $PROJECT_NAME | Set-Content "templates/base.html"
(gc "$PROJECT_NAME/settings.py") -replace "your.name@example.com", $MAINTAINER_EMAIL `
                                  -replace "example.com", $COMPANY_DOMAIN | Set-Content "$PROJECT_NAME/settings.py"
```


# Explanation of environment variables
| Variable name           | Goal                                                                             | What happens if empty?                                      | Default value                                                    |
|-------------------------|----------------------------------------------------------------------------------|-------------------------------------------------------------|------------------------------------------------------------------|
| SECRET_KEY              | signing sessions, cookies etc                                                    | the application is started in DEBUG mode with a default key | `openssl rand -base64 30`                                        |
| PORT                    | port on which the application is to listen                                       | default value is used                                       | `8080`                                                           |
| DOMAIN                  | easy including of images, links etc. in the emails                               | default value is used                                       | `127.0.0.1:{PORT}`                                               |
| TZ                      | specifying the applications timezone                                             |                                                             | `UTC`                                                            |
| EMAIL_USE_TLS           | specifying whether to send emails using TLS                                      | default value is used                                       | `False`                                                          |
| EMAIL_HOST              | specifying the host of the SMTP server’s                                         | emails are stored in files instead of being sent            | N/A                                                              |
| EMAIL_PORT              | specifying the SMTP server’s port                                                | default value is used                                       | `26`                                                             |
| EMAIL_HOST_USER         | specifying the SMTP server user                                                  | default value is used                                       | N/A                                                              |
| EMAIL_HOST_PASSWORD     | specifying the SMTP server user’s password                                       | default value is used                                       | N/A                                                              |
| DEFAULT_FROM_EMAIL      | specifying the default email from which the application sends message            | default value is used                                       | `{{ project_name\|title }}Bot <{{ project_name }}@domain.com`    |
| SERVER_EMAIL            | specifying the default email from which the applications send emails with errors | default value is used                                       | `{{ project_name\|title }}Errors <{{ project_name }}@domain.com` |
| DJANGO_LOCALE           | specifying the applications language                                             | default value is used                                       | `en-us`                                                          |
| USE_THOUSAND_SEPARATOR  | specifying whether to use a thousand separator                                   | default value is used                                       | `True`                                                           |
| STATIC_ROOT             | specifying the folder with static files when DEBUG is False                      | default value is used                                       | `/var/www/{{ project_name }}/static`                             |

# List of custom django system checks
 - `django_robust_template.J001` - emits an error if a first-party model dose not specify `verbose_name`. This is so the field's
 name is nicely displeyd when rendering forms, in admin etc.
 - `django_robust_template.J002` - emits an error if a first-party model field's does not specify `db_comment`. This is so
 each field is somewhat documented
 - `django_robust_template.J003` - emits an error if a first-party model's field does not explicitly specify `null` argument. 
 This is since [explicit is better than implicit](https://peps.python.org/pep-0020/)
 - `django_robust_template.J004` - emits an error if a first-party model's field does not explicitly specify `blank` argument.
 This is since [explicit is better than implicit](https://peps.python.org/pep-0020/)
 - `django_robust_template.J005` - emits a warning if a first-party model's CharField does not explicitly.
 specify `max_length` argument. This is since [explicit is better than implicit](https://peps.python.org/pep-0020/)
 - `django_robust_template.J006` - emits a warning if a first-party model's field `db_comment` argument contains
 non-ascii characters. This is since some databases might throw odd errors if the comment contains non-ascii text.
 - `django_robust_template.J007` - emits a warning if a first-party model's `BooleanField` dose not explicitly define
 the `default` argment. This is since a `BooleanField` by [default allows None which is probably not desired](https://docs.djangoproject.com/en/{{ docs_version }}/ref/models/fields/#booleanfield) and since [explicit is better than implicit](https://peps.python.org/pep-0020/)
 - `django_robust_template.J008` - emits a warning if a first-party models's field specfies a `default` argument but
 not the [`db_default`](https://docs.djangoproject.com/en/{{ docs_version }}/ref/models/fields/#db-default) argument. This is since
 if the database is ETL outside of django context, we'd like the default value to also be present.
 - `django_robust_template.J009` - emits an error if a first-party model's ForeingKey or ManyToManyField 
 dose not explicitly specify the `related_name` argument. This is since [explicit is better than implicit](https://peps.python.org/pep-0020/)
 - `django_robust_template.J010` - emits an error if a first-party model's ForeingKey or ManyToManyField dose not
 explicitly specify the `related_query_name` argument. This is since [explicit is better than implicit](https://peps.python.org/pep-0020/)
 - `django_robust_template.J011` - emits an error if a first-party model has no explicitly defiend `Meta`. This is
 since [explicit is better than implicit](https://peps.python.org/pep-0020/)
 - `django_robust_template.J012` - emits an error if a first-party model's field dose not specify `help_text` argument.
 This is since I belive that most form fields become easier to understand with `help_text`.
 - `django_robust_template.J013` - emits an error if a first-party model has no explicitly specified `editable` argument.
 This is since by default, `editable=True` and [explicit is better than implicit](https://peps.python.org/pep-0020/).
 - `django_robust_template.J014` - emits an error if a first-party model dose not explicitly specify `verbose_name` in
 its `Meta`. This is to provide better interoperability (working as expected, out of the box) with admin etc. and since [explicit is better than implicit](https://peps.python.org/pep-0020/) and [django sets a defuault `verbose_name`](https://docs.djangoproject.com/en/{{ docs_version }}/ref/models/options/#verbose-name).
 - `django_robust_template.J015` - emits an error if a first-party model has no explicitly specified
 `verbose_name_plural` in its `Meta`. This is to provide better interoperability with admin etc. and since
 [explicit is better than implicit](https://peps.python.org/pep-0020/) and [django sets a default `verbose_name_plural`](https://docs.djangoproject.com/en/{{ docs_version }}/ref/models/options/#verbose-name-plural)
 - `django_robust_template.J016` - emits an error if a first-party model has no `db_table_comment` specified in its
 Meta. This is so each table is somehow documented.
 - `django_robust_template.J017` - emits a warning if a first-party model's `db_table_comment` is non-ascii. This is
 since some databases might throw odd errirs if the comment contains non-ascii text.
 - `django_robust_template.J018` - emits an error if a first-party models has no `db_table` specified in its `Meta`.
 This is so to ensure all of the tables used by the django follow a naming convention (e.g. are prefixed with the
 program's name).
 - `django_robust_template.J019` - emits an error if a first-party model's ManyToManyField dose not explicitly specify 
 the `db_table` argument. This is to ensure tables used by the program follow a naming convetion and since [explicit is better than implicit](https://peps.python.org/pep-0020/)
 - `django_robust_template.J020` - emits an error if a first-party model has not `default_permissions` specified in
 its `Meta`. This is so to ensure the table with permissions isn't needlesl cluttered [(django creates some permission by default)](https://docs.djangoproject.com/en/{{ docs_version }}/ref/models/options/#default-permissions) and since [explicit is better than implicit](https://peps.python.org/pep-0020/)
 - `django_robust_template.J021` - emits a warning if a first-party model does not contain a field named
 `last_modified_at`. This is since I consider such field useful to have on *all* models.
 - `django_robust_template.J022` - emits a warning if a first-party model dose not explicitly specify a `__str__`
 method. This is since [explicit is better than implicit](https://peps.python.org/pep-0020/) and to ensure better 
 interoperability with admin etc.
 - `django_robust_template.J023` - emits a warning if a first-party mdoel does not explicitly specify a `__repr__`
 method. This is since I conside such method useful for debugging.
 - `django_robust_template.J024` - emits a warning if a first-party model does not specify a `get_absoulte_url`
 method. This is to improve interoperability with django.

Please keep in mind that using this specific set of checks is highly subjective  -- if you feel like 
any of the is stupid, you can to remove any of the from `checks.py` or disable any of them by specifying 
`SILENCED_SYSTEM_CHECKS` in your `settings.py`, e.g:

```python
SILENCED_SYSTEM_CHECKS = [
    'models.J019',
]
```


# Default design

![Preview of the default design](preview.png)

