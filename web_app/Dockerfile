FROM python:3.13.3-alpine@sha256:18159b2be11db91f84b8f8f655cd860f805dbd9e49a583ddaac8ab39bf4fe1a7

# Prevent Python from writing pyc files and enable unbuffered output
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends build-essential && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the rest of the application code
COPY . .

# Set environment variables for Streamlit
ENV PORT=8501
EXPOSE 8501

# Run the Streamlit web app on startup
CMD ["streamlit", "run", "src/app.py", "--server.port", "8501", "--server.address", "0.0.0.0"]
