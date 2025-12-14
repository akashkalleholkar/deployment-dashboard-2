FROM python:3.11-slim
WORKDIR /code

# Add required system deps (build-essential already present)
RUN apt-get update && apt-get install -y \
    build-essential \
    default-libmysqlclient-dev \
    libssl-dev \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
EXPOSE 90
CMD ["python", "-m", "app.server"]
