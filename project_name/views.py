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
