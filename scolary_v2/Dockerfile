# Use an official Python runtime as a parent image
FROM python:3.10

# Set environment variables to prevent interactive prompts and ensure logs flush
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV TESTING=0

# Set the working directory
WORKDIR /app

# Install system dependencies (DB client, WeasyPrint + Chromium deps, fonts)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    build-essential \
    libnss3 \
    libxss1 \
    libasound2 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libdrm2 \
    libgbm1 \
    libgtk-3-0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libcairo2 \
    libcups2 \
    libxrandr2 \
    libxkbcommon0 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libatspi2.0-0 \
    libxshmfence1 \
    libgdk-pixbuf-2.0-0 \
    fonts-liberation \
    fonts-noto-color-emoji \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt \
    && python -m playwright install chromium

# Copy test files and application code
COPY ./tests /app/tests
COPY ./app /app/app
COPY ./alembic /app/alembic
COPY ./alembic.ini /app/alembic.ini
COPY ./main.py /app/main.py
COPY ./prestart.sh /app/prestart.sh
COPY ./backend_pre_start.py /app/backend_pre_start.py
COPY ./initial_data.py /app/initial_data.py
COPY ./run_tests.sh /app/run_tests.sh

# Make scripts executable
RUN chmod +x /app/prestart.sh /app/run_tests.sh

# Expose the application port
EXPOSE 8081

# Start the application
ENTRYPOINT ["sh", "/app/prestart.sh"]
