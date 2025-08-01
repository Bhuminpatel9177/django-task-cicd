# Use a stable Python version
FROM python:3.13

# Set working directory inside container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y python3-distutils python3-pip && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip install --upgrade pip

# Copy requirements.txt only if it exists
COPY requirements.txt . 

# Install dependencies only if requirements.txt exists
RUN test -f requirements.txt && pip install -r requirements.txt || echo "Skipping pip install, no requirements.txt found"

# Copy project files into the container
COPY . .

# Expose port 8000 for Django
EXPOSE 8000

# Run migrations and start server
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]