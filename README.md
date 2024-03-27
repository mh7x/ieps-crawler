# Crawler for IEPS project

A brief description of what this project does and who it's for

## Docker setup

To build and run Docker container, run:

```bash
  docker build -t webcrawler .
  docker run -p 8888:8888 -v ${PWD}/:/app --name webcrawler-container -d webcrawler
```

then open localhost:8888 in your browser to access Jupyter.