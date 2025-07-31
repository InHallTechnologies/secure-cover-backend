FROM python:3.12-bookworm

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    rustc \
    curl \
    libffi-dev \
    libssl-dev \
    python3-dev \
    pkg-config \
    && apt-get clean

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get install -y ntp

COPY . .

EXPOSE 8080
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]
