FROM python:3.11-slim

# Install system dependencies and curl for uv installer
RUN apt-get update && apt-get install -y \
    gcc \
    libffi-dev \
    python3-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install uv using official installer (ensures correct architecture)
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# Add uv to PATH
ENV PATH="/root/.local/bin:$PATH"

# Copy project files
COPY pyproject.toml uv.lock ./
COPY src/ ./src/
COPY main.py ./

# Install dependencies
RUN uv sync --frozen

# Run the bot
CMD ["uv", "run", "main.py"]
