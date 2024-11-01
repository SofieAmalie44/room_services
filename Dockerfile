# Use official lightweight Python image
FROM python:3.9

# Setting working directory in the container
WORKDIR /app

# Copy the requirements file first for dependency caching
COPY requirements.txt .

# install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files into the container
COPY . .

# Port that Flask uses
EXPOSE 5004

# Set environment variable to make sure that Flask runs in production mode by default
ENV FLASK_ENV=production

# Run the application
CMD ["python", "app.py"]
