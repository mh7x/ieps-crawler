# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /usr/src/app

RUN apt-get update && apt-get install -y \
    firefox-esr \
    && rm -rf /var/lib/apt/lists/*

# Install GeckoDriver
RUN apt-get update && apt-get install -y wget \
    && wget https://github.com/mozilla/geckodriver/releases/download/v0.34.0/geckodriver-v0.34.0-linux64.tar.gz \
    && tar -xvzf geckodriver-v0.34.0-linux64.tar.gz \
    && mv geckodriver /usr/local/bin \
    && rm geckodriver-v0.34.0-linux64.tar.gz

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install any needed packages specified in requirements.txt or directly
RUN pip install --no-cache-dir requests beautifulsoup4 psycopg2-binary PyPDF2 python-docx python-pptx selenium urllib3

# Make port 80 available to the world outside this container
EXPOSE 80

# Run crawler.py when the container launches
CMD ["python", "./main.py"]
