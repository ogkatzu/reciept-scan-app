# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY main.py /app/
COPY requirements.txt /app/
COPY static /app/static/
COPY templates /app/templates
COPY proccess.py /app/

# Install Tesseract and Hebrew language support
RUN apt-get update && \
    apt-get install -y tesseract-ocr tesseract-ocr-heb && \
    rm -rf /var/lib/apt/lists/*

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV FLASK_APP=main.py

# Copy additional files and folders
COPY templates /app/templates
COPY static /app/static

# Run flask app when the container launches
CMD ["flask", "run", "--host=0.0.0.0", "--port=80"]
