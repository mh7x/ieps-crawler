# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir requests beautifulsoup4 psycopg2-binary PyPDF2 python-docx python-pptx selenium urllib3

# Make port 80 available to the world outside this container
EXPOSE 80

# Run crawler.py when the container launches
CMD ["python", "./main.py"]