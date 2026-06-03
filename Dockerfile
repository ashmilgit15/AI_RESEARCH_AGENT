# Step 1: Use an official lightweight Python system base image
FROM python:3.11-slim

# Step 2: Install system dependencies required by WeasyPrint
# Step 2: Install system dependencies required by WeasyPrint
RUN apt-get update && apt-get install -y \
    libpango-1.0-0 \
    libharfbuzz0b \
    libpangoft2-1.0-0 \
    libffi-dev \
    libjpeg-dev \
    libopenjp2-7-dev \
    shared-mime-info \
    libgdk-pixbuf-2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Step 3: Set up your working directory inside the container
WORKDIR /app

# Step 4: Copy package files and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Copy the rest of your local application files
COPY . .

# Step 6: Expose port 8000 for web traffic redirection
EXPOSE 8000

# Step 7: Launch the FastAPI server process via Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]