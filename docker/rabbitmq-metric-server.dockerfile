# syntax = docker/dockerfile:experimental
FROM python:3.7-slim

# Set Timezone
ENV TZ=UTC
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Install dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        libgtk2.0-dev \
        gcc && \
    apt-get clean

# Set virtualenv
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy common modules
COPY packages/ app/

# Install requirements
COPY apps/rabbitmq-metric-server/requirements.txt .
RUN --mount=type=cache,target=/root/.cache \
    pip install -r requirements.txt

# Copy package
COPY apps/rabbitmq-metric-server/app/ app/

# Create user
RUN useradd user

# Run app
ENV PATH="/opt/venv/bin:$PATH"
CMD ["uwsgi", "--ini", "app/uwsgi.ini", "--enable-threads"]