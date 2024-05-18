# Dockerfile for Python Backend
FROM python:3.12-bookworm

# Install ffmpeg
RUN apt-get -y update && apt-get -y upgrade && apt-get install -y --no-install-recommends ffmpeg

# Install Poetry
RUN pip install poetry

# Set the working directory
WORKDIR /backend

# Copy the Poetry configuration files
COPY pyproject.toml poetry.lock* ./

# Install dependencies without creating a virtual environment
RUN poetry install --no-interaction

# Expose the necessary port
EXPOSE 8000

# Command to run the application
CMD poetry run uvicorn spectral.main:app --host 0.0.0.0 --proxy-headers --reload --timeout-graceful-shutdown 2
