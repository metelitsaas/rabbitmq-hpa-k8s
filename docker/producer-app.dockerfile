FROM python:3.7-slim

# Set Timezone
ENV TZ=UTC
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Set virtualenv
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install requirements
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy package
COPY app/ app/

# Run app
ENV PATH="/opt/venv/bin:$PATH"
ENV PYTHONPATH="/app"
CMD ["python", "app"]