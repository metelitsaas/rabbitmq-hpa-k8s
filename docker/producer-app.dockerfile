# syntax = docker/dockerfile:experimental
FROM python:3.7-slim

# Set Timezone
ENV TZ=UTC
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Set virtualenv
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy common modules
COPY packages/ app/

# Install requirements
COPY apps/producer-app/requirements.txt .
RUN --mount=type=cache,target=/root/.cache \
    pip install -r requirements.txt

# Copy application
COPY apps/producer-app/app/ app/

# Run app
ENV PATH="/opt/venv/bin:$PATH"
ENV PYTHONPATH="/app"
CMD ["python", "app"]