from http import HTTPStatus

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.views.decorators.http import require_GET
from django.contrib.auth.decorators import login_required


@require_GET
@login_required
def home(request: HttpRequest) -> HttpResponse:
    return render(
        request,
        template_name='home.html',
    )


def handle_error_401(
    request: HttpRequest,
    exception: BaseException,
) -> HttpResponse:
    return render(
        request,
        template_name='401.html',
    )


def handle_error_403(
    request: HttpRequest,
    exception: BaseException,
) -> HttpResponse:
    return render(
        request,
        template_name='403.html',
        status=HTTPStatus.FORBIDDEN,
    )


def handle_error_404(
    request: HttpRequest,
    exception: BaseException,
) -> HttpResponse:
    return render(
        request,
        template_name='404.html',
        status=HTTPStatus.NOT_FOUND,
    )


def handle_error_500(request: HttpRequest) -> HttpResponse:
    return render(
        request,
        template_name='500.html',
        status=HTTPStatus.INTERNAL_SERVER_ERROR,
    )

