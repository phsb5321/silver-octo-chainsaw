# Base image with your specific Python version
FROM python:3.10-slim AS base

# Set essential environment variables to:
# - Ensure Python output goes straight to the terminal (without buffering)
# - Prevent Python from generating .pyc files
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    # Set Python PATH to find the installed packages
    PYTHONPATH=/usr/src/app

# Set the working directory to /usr/src/app
WORKDIR /usr/src/app

# Install poetry using pip and update pip to the latest version
# We use `--no-cache-dir` to keep the image small
# The virtual environment is not needed in the container,
# so we disable its creation.
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir poetry && \
    poetry config virtualenvs.create false

# Install netcat-openbsd for network utilities (like checking if the DB is up)
RUN apt-get update && apt-get install -y netcat-openbsd && rm -rf /var/lib/apt/lists/*

# Copy only Poetry configuration files first to cache this layer,
# this layer will be rebuilt only if pyproject.toml or poetry.lock change.
COPY pyproject.toml poetry.lock* ./

# Install the project dependencies
# We use `--no-interaction` and `--no-ansi` to not require interaction
# during the build process and to avoid ANSI output.
# `--no-dev` is used to prevent installing dev dependencies.
RUN poetry install --no-root --no-dev --no-interaction --no-ansi

# Copy your application code to the /usr/src/app folder in the container
# Copy your application code and entrypoint script
COPY . .
COPY entrypoint.sh .

# Give execution rights on the entrypoint script
RUN chmod +x /usr/src/app/entrypoint.sh

# Set the entrypoint script to be executed
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]

# Set the default command to execute the application using the Python module syntax
CMD ["python", "-m", "app.main"]