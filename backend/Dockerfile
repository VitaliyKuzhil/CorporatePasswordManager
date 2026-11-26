# syntax=docker/dockerfile:1

# Set root image
FROM python:3.11-slim

# Set image metadata
LABEL authors="Vitalii Kuzhil"
LABEL version="1.0"

# Set work directory for container
WORKDIR /app

# Set settings environments
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Copy only requirements to docker cache
COPY requirements.txt .

# Run command into container (Install dependencies)
RUN pip install --no-cache-dir -r requirements.txt

RUN useradd --create-home --uid 10001 appuser

# Copy project into WORKDIR
COPY --chown=appuser:appuser src/ src/
COPY --chown=appuser:appuser migrations/ migrations/
COPY alembic.ini .

# Open port for FastAPI
EXPOSE 8000

USER appuser

# Run commands
CMD ["sh", "-c", "alembic upgrade head && exec uvicorn src.main:app --host 0.0.0.0 --port 8000"]
