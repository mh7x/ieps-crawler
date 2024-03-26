# Crawler for IEPS project

A brief description of what this project does and who it's for

## Docker setup

To build and run Docker container, run:

```bash
  docker build -t webcrawler .
  docker run -p 8888:8888 -v ${PWD}/:/app --name webcrawler-container -d webcrawler
  docker exec -it webcrawler-container bash -c "conda run -n wier jupyter notebook list" 
```

then open localhost:8888 in your browser and copy the token from terminal to set your password for Jupyter.