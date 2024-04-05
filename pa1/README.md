# Crawler for IEPS project

This is the web crawler made by Nejc Rihter, Tomaž Dagaj and Tadej Lenart for the IEPS course of the BMA program at FRI.
There are two ways to run this crawler, you may run it using python or run it using docker.

## Run the crawler with python

To run the crawler with python you must first install all needed dependencies with pip.
```python
pip install requests bs4 urllib3 psycopg2 PyPDF2 python-docx python-pptx selenium
```

Then simply run it using
```python
python main.py
```
You will then be prompted to input the number of threads. And the crawler will run.

## Run the crawler with docker
To run the crawler using docker issue the following commands.
```bash
docker pull nejcrihter/spider:maybe12
docker run -d --restart always nejcrihter/spider:maybe12
````
Before this don't forget to set the number of theads in the code to the desired number of threads.
This command will ensure the crawler restarts should anything happen.