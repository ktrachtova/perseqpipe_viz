# Use the official lightweight Python image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
# Default Streamlit port
ENV PORT=8502

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libopenblas-dev \
    libpng-dev \
    libfreetype6-dev \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Create a working directory
WORKDIR /app

# Install Python dependencies
RUN pip install --no-cache-dir \
    streamlit==1.50.0 \
    pandas==2.2.3 \
    plotly==6.3.1 \
    seaborn==0.13.2 \
    matplotlib==3.9.4 \
    scikit-learn==1.6.1 \
    kaleido==0.2.1 \
    biopython==1.84 \
    pysam==0.22.1

# Copy the app code into the container
COPY .. .

# Default command uses the PORT env variable
CMD ["bash", "-c", "streamlit run app.py --server.port=$PORT --server.address=0.0.0.0"]