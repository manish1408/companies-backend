# Use the official Python 3.11.4 image from the Docker Hub
FROM python:3.11.4-slim

# Set the working directory in the container
WORKDIR /

# Copy the requirements.txt file into the container at /
COPY requirements.txt /

# Install any dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . /

# Expose the port that the FastAPI app runs on
EXPOSE 8000

# Command to run the FastAPI application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]