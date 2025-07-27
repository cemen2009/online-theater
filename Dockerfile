FROM python:3:13-slim

# Environment variables

#prevents .pyc generation
ENV PYTHONDONTWRITEBYTECODE=1 \
    # disables output buffering for logs
    PYTHONUNBUFFERED=1 \
    # retains pip cache unless explicitly cleared
    PIP_NO_CACHE_DIR=off \
    # suppresses pip version warnings
    PIP_DISABLE_PIP_VERSION_CHECK=on

# System dependencies

# installs dos2unix for scripts compability
# cleans APT cache to reduce layer size
RUN apt update && apt install -y --no-install-recommends \
    dos2unix \
    && apt clean && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /usr/src/fastapi

# Install Python dependencies
COPY ./requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy application source
COPY ./src .

# Copy and prepare shell scripts
COPY ./commands /commands
# converts line endings, sets executable permissions
RUN dos2unix /commands/*.sh && chmod +x /commands/*.sh