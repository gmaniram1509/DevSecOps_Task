FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV DJANGO_SETTINGS_MODULE=task_manager.settings_production

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    libpq-dev \
    gcc \
    python3-dev \
    musl-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements_aws.txt /app/
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements_aws.txt && \
    pip install gunicorn

# Copy project files
COPY . /app/

# Create necessary directories
RUN mkdir -p /app/staticfiles /app/media /var/log/django

# Collect static files
RUN python manage.py collectstatic --noinput || true

# Create non-root user
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app /var/log/django

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=40s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/admin/', timeout=2)" || exit 1

# Run gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "--timeout", "120", "--access-logfile", "-", "--error-logfile", "-", "task_manager.wsgi:application"]

