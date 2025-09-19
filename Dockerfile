# Use NVIDIA CUDA image as base with Python 3.11
FROM nvidia/cuda:13.0.1-cudnn-runtime-ubuntu22.04

# Install Python 3.11
RUN apt-get update && apt-get install -y \
    software-properties-common \
    && add-apt-repository ppa:deadsnakes/ppa \
    && apt-get update && apt-get install -y \
    python3.11 \
    python3.11-dev \
    python3.11-distutils \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Set Python 3.11 as default
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.11 1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    libgcc-s1 \
    tesseract-ocr \
    tesseract-ocr-fra \
    poppler-utils \
    libmagic1 \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV CUDA_VISIBLE_DEVICES=0
ENV TRANSFORMERS_CACHE=/app/models
ENV HF_HOME=/app/models

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN python3 -m pip install --no-cache-dir --upgrade pip && \
    python3 -m pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY handler.py .
COPY docling_handler.py .

# Create necessary directories
RUN mkdir -p /app/temp /app/models /app/logs

# Set permissions
RUN chmod +x /app/handler.py

# Runpod serverless entry point
CMD ["python3", "handler.py"]
