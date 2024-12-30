# Use Python 3.9 slim image as base
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . .

# Create necessary directories if they don't exist
RUN mkdir -p config data

# Create volume mount points for sensitive data
VOLUME ["/app/config", "/app/data", "/app/credentials.json", "/app/token.json"]

# Environment variables (these should be overridden at runtime)
ENV EMAIL_ADDRESS=""
ENV EMAIL_PASSWORD=""
ENV OPENAI_API_KEY=""

# Run the application
CMD ["python", "-m", "src.main"]

# Add healthcheck
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD python -c "import os; exit(0 if os.path.exists('token.json') else 1)"