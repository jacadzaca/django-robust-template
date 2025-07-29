FROM python:3.11 AS compile-image

ENV TZ="Europe/London"

# https://pythonspeed.com/articles/activate-virtualenv-dockerfile/
ENV PATH="/opt/venv/bin:$PATH"

RUN apt-get update -y \
    && apt-get --no-install-recommends -f install -y python3-dev libev-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN python -m venv /opt/venv \
    && pip install --upgrade pip \
    && pip install -r requirements.txt

FROM python:3.11-slim
LABEL org.opencontainers.image.authors="your.email@example.com"
LABEL org.opencontainers.image.vendor="Your company"
LABEL org.opencontainers.image.description="Your application's description"
LABEL org.opencontainers.image.base.name="docker.io/python:3.11"

ENV PYTHONBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PATH="/opt/venv/bin:$PATH"
ENV TZ="Europe/London"

WORKDIR /home/{{ project_name }}

COPY --from=compile-image /opt/venv /opt/venv
COPY . /home/{{ project_name }}

RUN apt-get update -y \
    && apt-get --no-install-recommends -f install -y libev-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && useradd -ms /bin/bash {{ project_name }} \
    && mkdir -p /var/www/{{ project_name }}/static \
    && python manage.py collectstatic --clear --noinput \
    && chown -R {{ project_name }}:{{ project_name }} /var/www/ \
    && chown -R {{ project_name }}:{{ project_name }} /home/{{ project_name }}

USER {{ project_name }}

ENTRYPOINT ["/bin/bash", "startup.sh"]

