# Use an official Miniconda image as a base
FROM continuumio/miniconda3

# Set up working directory
WORKDIR /app

# Copy environment file
COPY environment.yml /app/environment.yml

# Create and activate Conda environment
RUN conda env create -f environment.yml
SHELL ["conda", "run", "-n", "wier", "/bin/bash", "-c"]

# Copy the rest of the application code into the container
COPY . /app

# Expose any ports your application listens on
EXPOSE 8888

# Command to run PostgreSQL and Jupyter notebook
CMD conda run -n wier jupyter notebook --ip='0.0.0.0' --port=8888 --no-browser --allow-root --NotebookApp.token="" --NotebookApp.password=""