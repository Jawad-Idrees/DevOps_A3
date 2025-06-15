# Use the official Python image from the Docker Hub
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the container at /app
COPY requirements.txt .

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    gfortran \
    musl-dev \
    libffi-dev \
    libopenblas-dev \
    liblapack-dev \
    libfreetype6-dev \
    libpng-dev \
    libxml2-dev \
    libxslt-dev \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    libjpeg-dev \
    libhdf5-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables for OpenBLAS and LAPACK
ENV BLAS=/usr/lib/libopenblas.so
ENV LAPACK=/usr/lib/liblapack.so
RUN pip install itsdangerous
# Install Python dependencies
RUN pip install --upgrade pip && pip install --default-timeout=100 -r requirements.txt


# Copy the rest of the working directory contents into the container at /app
COPY . .

# Expose the port that the app runs on
EXPOSE 8001

# Set default values for environment variables



# Run the FastAPI app using uvicorn
CMD ["uvicorn", "main2:app","--host","0.0.0.0", "--port", "8001"]














































# # Use the official Python image from the Docker Hub
# FROM python:3.10-slim

# # Set the working directory in the container
# WORKDIR /app

# # Copy the requirements.txt file into the container at /app
# COPY requirements.txt .

# # Install system dependencies
# RUN apt-get update && apt-get install -y \
#     build-essential \
#     cmake \
#     gfortran \
#     musl-dev \
#     libffi-dev \
#     libopenblas-dev \
#     liblapack-dev \
#     libfreetype6-dev \
#     libpng-dev \
#     libxml2-dev \
#     libxslt-dev \
#     libjpeg62-turbo-dev \
#     zlib1g-dev \
#     libjpeg-dev \
#     libhdf5-dev \
#     && apt-get clean \
#     && rm -rf /var/lib/apt/lists/*

# # Install Linux headers for WSL2 (specific to WSL2 kernel)
# RUN pip install itsdangerous

# # Set environment variables for OpenBLAS and LAPACK
# ENV BLAS=/usr/lib/libopenblas.so
# ENV LAPACK=/usr/lib/liblapack.so

# # Install Python dependencies
# RUN pip install -r requirements.txt

# # Copy the rest of the working directory contents into the container at /app
# COPY . .

# # Expose the port that the app runs on
# EXPOSE 8001

# # Run the FastAPI app using uvicorn
# CMD ["uvicorn", "main2:app", "--host", "eastransferapp3.azurewebsites.net", "--port", "8001"]
